import mysql.connector
from mysql.connector import Error
import xmlrpc.client
from typing import List, Dict, Union, Tuple
from colorama import init, Fore, Style
from tqdm import tqdm
init(autoreset=True)

class OdooData:
    def __init__(self):
        self.url = '<ODOO_URL>'
        self.db = '<ODOO_DATABASE>'
        self.username = '<ODOO_USERNAME>'
        self.password = '<ODOO_PASSWORD>'

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        self.uid = common.authenticate(self.db, self.username, self.password, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))

    def empleados(self):
        fields = [
            'id', 'display_name', 'image_1920', 'company_id', 'resource_calendar_id',
            'job_title', 'work_phone', 'mobile_phone', 'work_email',
            'gender', 'marital', 'create_date', 'identification_id',
            'birthday', 'barcode', 'private_street'
        ]

        empleados = self.models.execute_kw(
            self.db,
            self.uid,
            self.password,
            'hr.employee',
            'search_read',
            [],
            {'fields': fields}
        )
        return empleados

    def productos(self):
        fields = [
            'id', 'name', 'description', 'image_1920', 'list_price', 'standard_price',
            'detailed_type', 'categ_id', 'qty_available', 'sale_ok', 'purchase_ok',
            'barcode', 'default_code', 'uom_id', 'active', 'available_in_pos'
        ]

        productos = self.models.execute_kw(
            self.db,
            self.uid,
            self.password,
            'product.product',
            'search_read',
            [[]],
            {'fields': fields}
        )
        return productos

    def ventas(self) -> Tuple[List[Dict[str, Union[int, str]]], List[Dict[str, Union[int, str]]], Dict[str, Dict[str, int]]]:
        fields = [
            'id', 'date_order', 'amount_total', 'company_id', 'partner_id', 'lines'
        ]

        ventas = self.models.execute_kw(
            self.db,
            self.uid,
            self.password,
            'pos.order',
            'search_read',
            [[]],
            {'fields': fields}
        )

        detalles_venta = []
        company_dict = {}
        partner_dict = {}

        for venta in ventas:
            company_id = venta['company_id'][0] if venta['company_id'] else None
            company_name = venta['company_id'][1] if venta['company_id'] else None
            partner_id = venta['partner_id'][0] if venta['partner_id'] else None
            partner_name = venta['partner_id'][1] if venta['partner_id'] else None

            if company_id and company_name and company_id not in company_dict:
                company_dict[company_id] = company_name

            if partner_id and partner_name and partner_id not in partner_dict:
                partner_dict[partner_id] = partner_name

            line_ids = venta.get('lines', [])
            if line_ids:
                lines = self.models.execute_kw(self.db, self.uid, self.password, 'pos.order.line', 'search_read', [[['id', 'in', line_ids]]], {})
                for line in lines:
                    detalles_venta.append({
                        'venta_id': venta['id'],
                        'detalle_id': line['id'],
                        'producto_id': line['product_id'][0],
                        'precio_unitario': line['price_unit'],
                        'cantidad': line['qty'],
                        'subtotal': line['price_subtotal'],
                        'nombre_completo_producto': line['full_product_name']
                    })

        fac_venta = [{'id': venta['id'], 'date_order': venta['date_order'], 'amount_total': venta['amount_total'], 'company_id': venta['company_id'], 'partner_id': venta['partner_id']} for venta in ventas]

        return fac_venta, detalles_venta, {'company_id': company_dict, 'partner_id': partner_dict}

class MySQLDatabase:
    def __init__(self):
        self.host = 'sql5.freesqldatabase.com'
        self.database = 'sql5724450'
        self.user = 'sql5724450'
        self.password = 'TQrIxLf3Iv'
        self.port = 3306

    def open_connection(self):
        return mysql.connector.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port
        )

    def insert_dim_fecha(self, start_date, end_date):
        from datetime import timedelta
        dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
                'septiembre', 'octubre', 'noviembre', 'diciembre']
        meses_cortos = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago',
                        'sep', 'oct', 'nov', 'dic']

        connection = self.open_connection()
        cursor = connection.cursor()
        date_list = []
        current_date = start_date
        while current_date <= end_date:
            fecha_id = int(current_date.strftime('%Y%m%d'))
            fecha = current_date.strftime('%Y-%m-%d')
            dia = current_date.day
            mes = current_date.month
            anio = current_date.year
            dia_semana = current_date.isoweekday()
            nombre_dia_semana = dias_semana[dia_semana - 1]
            nombre_mes = meses[mes - 1]
            nombre_mes_corto = meses_cortos[mes - 1]
            anio_mes = f"{anio}-{mes:02d}"
            trimestre = f"T{((mes - 1) // 3) + 1}"
            es_fin_de_semana = dia_semana >= 6
            dia_anio = current_date.timetuple().tm_yday
            semana_anio = current_date.isocalendar()[1]
            es_dia_laborable = dia_semana <= 5

            date_list.append( (fecha_id, fecha, dia, mes, anio, dia_semana, nombre_dia_semana,
                            nombre_mes, nombre_mes_corto, anio_mes, trimestre,
                            es_fin_de_semana, dia_anio, semana_anio, es_dia_laborable) )
            current_date += timedelta(days=1)

        sql = """
        INSERT INTO dim_fecha
        (fecha_id, fecha, dia, mes, anio, dia_semana, nombre_dia_semana, nombre_mes, nombre_mes_corto, anio_mes, trimestre, es_fin_de_semana, dia_anio, semana_anio, es_dia_laborable)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            cursor.executemany(sql, date_list)
            connection.commit()
            print(f"Inserted {len(date_list)} dates into dim_fecha")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()


    def insert_dim(self, connection, table, data):
        cursor = connection.cursor()
        for row in data:
            placeholders = ', '.join(['%s'] * len(row))
            columns = ', '.join(row.keys())
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            try:
                cursor.execute(sql, tuple(row.values()))
            except mysql.connector.errors.IntegrityError as e:
                if "Duplicate entry" in str(e):
                    print(f"Skipping duplicate entry in {table}: {row}")
                else:
                    raise e
        connection.commit()
        cursor.close()

    def insert_empleados(self, empleados):
        connection = self.open_connection()
        empresa_dict = {}
        calendario_recursos_dict = {}

        for emp in empleados:
            empresa_id = emp['company_id'][0] if emp['company_id'] else None
            nombre_empresa = emp['company_id'][1] if emp['company_id'] else None

            calendario_recursos_id = emp['resource_calendar_id'][0] if emp['resource_calendar_id'] else None
            nombre_calendario = emp['resource_calendar_id'][1] if emp['resource_calendar_id'] else None

            if empresa_id and nombre_empresa and empresa_id not in empresa_dict:
                empresa_dict[empresa_id] = nombre_empresa

            if calendario_recursos_id and nombre_calendario and calendario_recursos_id not in calendario_recursos_dict:
                calendario_recursos_dict[calendario_recursos_id] = nombre_calendario

        # Insertar empresa_id en dim_empresa
        empresas = [{'empresa_id': k, 'nombre_empresa': v} for k, v in empresa_dict.items()]
        self.insert_dim(connection, 'dim_empresa', empresas)

        # Insertar calendario_recursos_id en dim_calendario_recursos
        calendarios = [{'calendario_recursos_id': k, 'nombre_calendario': v} for k, v in calendario_recursos_dict.items()]
        self.insert_dim(connection, 'dim_calendario_recursos', calendarios)

        cursor = connection.cursor()
        for emp in empleados:
            sql = """
            INSERT INTO dim_empleado (empleado_id, nombre_completo, imagen, empresa_id, calendario_recursos_id, titulo_trabajo, telefono_trabajo, telefono_movil, email_trabajo, genero, estado_civil, fecha_creacion, id_identificacion, fecha_nacimiento, codigo_barras, direccion_privada)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                emp['id'], emp['display_name'], emp['image_1920'], 
                emp['company_id'][0] if emp['company_id'] else None, 
                emp['resource_calendar_id'][0] if emp['resource_calendar_id'] else None, 
                emp['job_title'], emp['work_phone'] if emp['work_phone'] else None,
                emp['mobile_phone'] if emp['mobile_phone'] else None, emp['work_email'] if emp['work_email'] else None,
                emp['gender'] if emp['gender'] else None, emp['marital'], emp['create_date'],
                emp['identification_id'] if emp['identification_id'] else None, 
                emp['birthday'] if emp['birthday'] else None, 
                emp['barcode'] if emp['barcode'] else None, 
                emp['private_street'] if emp['private_street'] else None
            )
            try:
                cursor.execute(sql, values)
            except mysql.connector.errors.IntegrityError as e:
                if "Duplicate entry" in str(e):
                    print(f"Skipping duplicate entry in dim_empleado: {emp}")
                else:
                    raise e
        connection.commit()
        cursor.close()
        connection.close()

    def insert_productos(self, productos):
        connection = self.open_connection()
        categoria_dict = {}
        unidad_medida_dict = {}

        for prod in productos:
            categoria_id = prod['categ_id'][0] if prod['categ_id'] else None
            nombre_categoria = prod['categ_id'][1] if prod['categ_id'] else None

            unidad_medida_id = prod['uom_id'][0] if prod['uom_id'] else None
            nombre_unidad_medida = prod['uom_id'][1] if prod['uom_id'] else None

            if categoria_id and nombre_categoria and categoria_id not in categoria_dict:
                categoria_dict[categoria_id] = nombre_categoria

            if unidad_medida_id and nombre_unidad_medida and unidad_medida_id not in unidad_medida_dict:
                unidad_medida_dict[unidad_medida_id] = nombre_unidad_medida

        # Insertar categoria_id en dim_categoria
        categorias = [{'categoria_id': k, 'nombre_categoria': v} for k, v in categoria_dict.items()]
        self.insert_dim(connection, 'dim_categoria', categorias)

        # Insertar unidad_medida_id en dim_unidad_medida
        unidades = [{'unidad_medida_id': k, 'nombre_unidad_medida': v} for k, v in unidad_medida_dict.items()]
        self.insert_dim(connection, 'dim_unidad_medida', unidades)

        cursor = connection.cursor()
        for prod in productos:
            sql = """
            INSERT INTO dim_producto (producto_id, nombre, descripcion, imagen, precio_lista, precio_estandar, tipo_detallado, categoria_id, cantidad_disponible, venta_permitida, compra_permitida, codigo_barras, codigo_default, unidad_medida_id, activo, disponible_en_pos)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                prod['id'], prod['name'], prod['description'] if prod['description'] else None, 
                prod['image_1920'] if prod['image_1920'] else None, prod['list_price'], 
                prod['standard_price'], prod['detailed_type'], 
                prod['categ_id'][0] if prod['categ_id'] else None, prod['qty_available'], 
                prod['sale_ok'], prod['purchase_ok'], 
                prod['barcode'] if prod['barcode'] else None, prod['default_code'], 
                prod['uom_id'][0] if prod['uom_id'] else None, prod['active'], prod['available_in_pos']
            )
            try:
                cursor.execute(sql, values)
            except mysql.connector.errors.IntegrityError as e:
                if "Duplicate entry" in str(e):
                    print(f"Skipping duplicate entry in dim_producto: {prod}")
                else:
                    raise e
        connection.commit()
        cursor.close()
        connection.close()

    def insert_ventas(self, ventas, detalles_venta, dictionaries):
        from datetime import datetime
        connection = self.open_connection()
        empresa_dict = dictionaries['company_id']
        cliente_dict = dictionaries['partner_id']
        # Insertar empresa_id en dim_empresa
        empresas = [{'empresa_id': k, 'nombre_empresa': v} for k, v in empresa_dict.items()]
        self.insert_dim(connection, 'dim_empresa', empresas)
        print(f"{Fore.CYAN}>Empresas insertadas correctamente")

        # Insertar cliente_id en dim_cliente
        clientes = [{'cliente_id': k, 'nombre': v} for k, v in cliente_dict.items()]
        self.insert_dim(connection, 'dim_cliente', clientes)
        print(f"{Fore.CYAN}>Clientes insertados correctamente")

        cursor = connection.cursor()
        for venta in tqdm(ventas, desc='Insertando ventas...'):
            sql = """
            INSERT INTO fact_venta (venta_id, fecha_id, fecha_venta, monto_total, empresa_id, cliente_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            fecha_venta = venta['date_order']
            fecha_id = int(datetime.strptime(fecha_venta, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d'))
            values = (
                venta['id'], fecha_id, venta['date_order'], venta['amount_total'], 
                venta['company_id'][0] if venta['company_id'] else None, 
                venta['partner_id'][0] if venta['partner_id'] else None
            )
            try:
                cursor.execute(sql, values)
                connection.commit()
                print(f"Entrada en fact_venta cargada correctamente: {venta['id']}")
            except mysql.connector.errors.IntegrityError as e:
                if "Duplicate entry" in str(e):
                    print(f"Skipping duplicate entry in fact_venta: {venta}")
                else:
                    print(e)
        
        for detalle in tqdm(detalles_venta, desc='Insertando detalles de ventas...'):
            sql = """
            INSERT INTO fact_detalle_venta (venta_id, detalle_id, producto_id, precio_unitario, cantidad, subtotal, nombre_completo_producto)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                detalle['venta_id'], detalle['detalle_id'], 
                detalle['producto_id'], 
                detalle['precio_unitario'], detalle['cantidad'], 
                detalle['subtotal'], detalle['nombre_completo_producto']
            )
            try:
                cursor.execute(sql, values)
                connection.commit()
                print(f"Entrada en fact_detalle_venta cargada correctamente: {detalle['detalle_id']} (Venta ID: {detalle['venta_id']})")
            except mysql.connector.errors.IntegrityError as e:
                if "Duplicate entry" in str(e):
                    print(f"Skipping duplicate entry in fact_detalle_venta: {detalle}")
                else:
                    print(f"{Fore.RED}{detalle}")
                    print(e)

        cursor.close()
        connection.close()

def main():
    print(f"{Fore.BLUE}Poblando base de datos...")
    odoo_data = OdooData()
    mysql_db = MySQLDatabase()

    # Poblar dim_fecha
    print(f"{Fore.GREEN}Poblando dim_fecha...")
    from datetime import datetime
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 12, 31)
    mysql_db.insert_dim_fecha(start_date, end_date)

    # Poblar empleados
    print(f"{Fore.GREEN}Poblando empleados...")
    empleados = odoo_data.empleados()
    mysql_db.insert_empleados(empleados)

    # Poblar productos
    print(f"{Fore.GREEN}Poblando productos...")
    productos = odoo_data.productos()
    mysql_db.insert_productos(productos)

    # Poblar ventas y detalles de ventas
    print(f"{Fore.GREEN}Poblando ventas y detalles de ventas...")
    ventas, detalles_venta, ventas_dictionaries = odoo_data.ventas()
    print(f"{Fore.CYAN}>Se han extraído {len(ventas)} ventas")
    print(f"{Fore.CYAN}>Se han extraído {len(detalles_venta)} detalles de ventas")
    mysql_db.insert_ventas(ventas, detalles_venta, ventas_dictionaries)

    print(f"{Fore.YELLOW}Datos poblados exitosamente")

if __name__ == '__main__':
    from datetime import datetime
    from create_database import main as create_database
    start = datetime.now()
    try:
        create_database()
        main()
    except Exception as e:
        print(f"{Fore.RED} {e}")
    finally:
        print(f"{Fore.CYAN}Tiempo de ejecución: {datetime.now() - start}")

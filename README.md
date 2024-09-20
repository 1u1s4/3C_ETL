# EPS_ETL

## Descripción

El proyecto **EPS_ETL** está diseñado para gestionar el proceso de **Extracción, Transformación y Carga (ETL)** de datos para la empresa Tres Cielos, una pastelería y panadería en expansión ubicada en Retalhuleu, Guatemala. Este proyecto automatiza la creación y populación de la base de datos MySQL necesaria para almacenar y analizar los datos operativos de Tres Cielos.

El proceso ETL incluye:

- **Extracción** de datos desde la plataforma Odoo utilizando XML-RPC.
- **Transformación** de los datos para adecuarlos al esquema del Data Warehouse.
- **Carga** de los datos transformados en una base de datos MySQL.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Scripts Principales](#scripts-principales)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)
- [Contacto](#contacto)

## Tecnologías Utilizadas

- **Lenguaje de Programación**: Python 3.x
- **Librerías**:
  - `mysql-connector-python`
  - `xmlrpc.client`
  - `colorama`
  - `tqdm`
- **Base de Datos**: MySQL
- **Control de Versiones**: Git

## Instalación

Sigue estos pasos para configurar y ejecutar el proyecto EPS_ETL en tu entorno local.

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/EPS_ETL.git
cd EPS_ETL
```

### 2. Crear un Entorno Virtual

Es recomendable utilizar un entorno virtual para gestionar las dependencias del proyecto.

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar las Dependencias

```bash
pip install -r requirements.txt
```

*Si no tienes un archivo `requirements.txt`, puedes instalar las siguientes librerías:*

```bash
pip install mysql-connector-python xmlrpc.client colorama tqdm
```

### 4. Configurar la Base de Datos

Asegúrate de tener acceso a la base de datos MySQL de Tres Cielos y de contar con las credenciales necesarias. Puedes configurar las variables de conexión directamente en los scripts o utilizar variables de entorno para mayor seguridad.

### 5. Configurar Variables de Entorno (Opcional)

Para mejorar la seguridad, es recomendable almacenar las credenciales de la base de datos en variables de entorno. Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
DB_HOST=<HOST>
DB_USER=<DB_USER>
DB_PASSWORD=<DB_PASSWORD>
DB_NAME=<DB_NAME>
DB_PORT=<DB_PORRT>
ODOO_URL=<URL>
ODOO_DB=<DB>
ODOO_USERNAME=<USERNAME>
ODOO_PASSWORD=<PASSWORD>
```

*Nota: Asegúrate de no subir este archivo al repositorio por razones de seguridad.*

## Uso

El proyecto EPS_ETL consta de varios scripts que automatizan el proceso ETL. A continuación, se describen brevemente los pasos para ejecutar cada uno.

### 1. Crear la Base de Datos y las Tablas

Ejecuta el script `create_database.py` para crear la base de datos y las tablas necesarias.

```bash
python create_database.py
```

### 2. Poblar la Base de Datos

Ejecuta el script `populate_database.py` para extraer datos de Odoo, transformarlos y cargarlos en la base de datos MySQL.

```bash
python populate_database.py
```

### 3. Gestionar Conexiones Activas

- **Cerrar todas las conexiones activas**:

  ```bash
  python kill_all_connections.py
  ```

- **Verificar conexiones activas**:

  ```bash
  python active_connections.py
  ```

## Estructura del Proyecto

```plaintext
EPS_ETL/
│
├── create_database.py
├── create_tables.sql
├── populate_database.py
├── kill_all_connections.py
├── active_connections.py
├── utils.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

- **create_database.py**: Script para crear la base de datos y las tablas necesarias.
- **create_tables.sql**: Archivo SQL con las definiciones de las tablas del Data Warehouse.
- **populate_database.py**: Script principal para extraer, transformar y cargar los datos desde Odoo a MySQL.
- **kill_all_connections.py**: Script para cerrar todas las conexiones activas a la base de datos.
- **active_connections.py**: Script para verificar el número de conexiones activas a la base de datos.
- **utils.py**: Funciones auxiliares utilizadas en el proceso ETL.
- **requirements.txt**: Lista de dependencias del proyecto.
- **README.md**: Este archivo.
- **.gitignore**: Archivos y carpetas a ignorar por Git.
- **LICENSE**: Información de licencia del proyecto.

## Scripts Principales

### create_database.py

Este script se encarga de conectarse a la base de datos MySQL y ejecutar el archivo `create_tables.sql` para crear las tablas necesarias.

### create_tables.sql

Contiene las definiciones SQL para las tablas del Data Warehouse, incluyendo dimensiones como `dim_empresa`, `dim_empleado`, `dim_producto`, `dim_cliente`, `dim_fecha`, `dim_categoria`, `dim_unidad_medida` y hechos como `fact_venta` y `fact_detalle_venta`.

### populate_database.py

Script principal que realiza el proceso ETL:

1. **Extracción**: Obtiene datos de empleados, productos y ventas desde Odoo utilizando XML-RPC.
2. **Transformación**: Procesa y organiza los datos para adecuarlos al esquema de la base de datos.
3. **Carga**: Inserta los datos transformados en las tablas correspondientes de MySQL.

### kill_all_connections.py

Cierra todas las conexiones activas a la base de datos MySQL, excepto la conexión actual. Esto es útil antes de realizar operaciones que requieren exclusividad en la base de datos.

### active_connections.py

Muestra el número actual de conexiones activas a la base de datos MySQL.

### utils.py

Contiene funciones auxiliares, como la decodificación y almacenamiento de imágenes de empleados.

## Contribuciones

Las contribuciones al proyecto son bienvenidas. Si deseas colaborar, por favor sigue estos pasos:

1. **Fork** el repositorio.
2. **Crea una rama** para tu feature (`git checkout -b feature/nueva-feature`).
3. **Commit** tus cambios (`git commit -m 'Añadir nueva feature'`).
4. **Push** a la rama (`git push origin feature/nueva-feature`).
5. **Crea un Pull Request** describiendo los cambios realizados.

## Licencia

Este proyecto está bajo la Licencia [Apache](LICENSE).

## Contacto

Si tienes alguna pregunta o necesitas más información, no dudes en contactarme:

- **Nombre**: Luis Alvarado

---

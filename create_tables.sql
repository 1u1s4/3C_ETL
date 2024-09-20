-- Desactivar las restricciones de clave foránea
SET FOREIGN_KEY_CHECKS = 0;

-- Recuperar todas las tablas y eliminarlas
SET @tables = NULL;
SELECT GROUP_CONCAT('`', table_name, '`') INTO @tables
FROM information_schema.tables 
WHERE table_schema = (SELECT DATABASE());

SET @tables = CONCAT('DROP TABLE IF EXISTS ', @tables);
PREPARE stmt FROM @tables;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Dimensiones
CREATE TABLE IF NOT EXISTS dim_empresa (
    empresa_id INT PRIMARY KEY,
    nombre_empresa VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS dim_calendario_recursos (
    calendario_recursos_id INT PRIMARY KEY,
    nombre_calendario VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS dim_empleado (
    empleado_id INT PRIMARY KEY,
    nombre_completo VARCHAR(255),
    imagen LONGBLOB,
    empresa_id INT,
    calendario_recursos_id INT,
    titulo_trabajo VARCHAR(255),
    telefono_trabajo VARCHAR(50),
    telefono_movil VARCHAR(50),
    email_trabajo VARCHAR(255),
    genero VARCHAR(10),
    estado_civil VARCHAR(50),
    fecha_creacion DATETIME,
    id_identificacion VARCHAR(50),
    fecha_nacimiento DATE,
    codigo_barras VARCHAR(50),
    direccion_privada VARCHAR(255),
    FOREIGN KEY (empresa_id) REFERENCES dim_empresa(empresa_id),
    FOREIGN KEY (calendario_recursos_id) REFERENCES dim_calendario_recursos(calendario_recursos_id)
);

CREATE TABLE IF NOT EXISTS dim_producto (
    producto_id INT PRIMARY KEY,
    nombre VARCHAR(255),
    descripcion TEXT,
    imagen LONGBLOB,
    precio_lista FLOAT,
    precio_estandar FLOAT,
    tipo_detallado VARCHAR(50),
    categoria_id INT,
    cantidad_disponible FLOAT,
    venta_permitida BOOLEAN,
    compra_permitida BOOLEAN,
    codigo_barras VARCHAR(50),
    codigo_default VARCHAR(50),
    unidad_medida_id INT,
    activo BOOLEAN,
    disponible_en_pos BOOLEAN,
    FOREIGN KEY (categoria_id) REFERENCES dim_categoria(categoria_id),
    FOREIGN KEY (unidad_medida_id) REFERENCES dim_unidad_medida(unidad_medida_id)
);

CREATE TABLE IF NOT EXISTS dim_cliente (
    cliente_id INT PRIMARY KEY,
    nombre VARCHAR(255),
    empresa_id INT,
    tipo VARCHAR(50),
    direccion VARCHAR(255),
    ciudad VARCHAR(255),
    estado_id INT,
    pais_id INT,
    email VARCHAR(255),
    telefono VARCHAR(50),
    movil VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_fecha (
    fecha_id INT PRIMARY KEY,
    fecha DATE,
    dia INT,
    mes INT,
    anio INT,
    dia_semana INT,
    nombre_dia_semana VARCHAR(20),
    nombre_mes VARCHAR(20),
    nombre_mes_corto VARCHAR(10),
    anio_mes VARCHAR(20),
    trimestre VARCHAR(10),
    es_fin_de_semana BOOLEAN,
    dia_anio INT,
    semana_anio INT,
    es_dia_laborable BOOLEAN
);

CREATE TABLE IF NOT EXISTS dim_categoria (
    categoria_id INT PRIMARY KEY,
    nombre_categoria VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS dim_unidad_medida (
    unidad_medida_id INT PRIMARY KEY,
    nombre_unidad_medida VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS fact_venta (
    venta_id INT PRIMARY KEY,
    fecha_id INT,
    fecha_venta DATETIME,
    monto_total FLOAT,
    empresa_id INT,
    cliente_id INT,
    FOREIGN KEY (empresa_id) REFERENCES dim_empresa(empresa_id),
    FOREIGN KEY (cliente_id) REFERENCES dim_cliente(cliente_id),
    FOREIGN KEY (fecha_id) REFERENCES dim_fecha(fecha_id)
);

CREATE TABLE IF NOT EXISTS fact_detalle_venta (
    venta_id INT,
    detalle_id INT PRIMARY KEY,
    producto_id INT,
    precio_unitario FLOAT,
    cantidad FLOAT,
    subtotal FLOAT,
    nombre_completo_producto VARCHAR(255),
    FOREIGN KEY (venta_id) REFERENCES fact_venta(venta_id),
    FOREIGN KEY (producto_id) REFERENCES dim_producto(producto_id)
);

-- Reactivar las restricciones de clave foránea
SET FOREIGN_KEY_CHECKS = 1;

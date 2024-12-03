# Rebeca Edith Silva Gutierrez 
# Sistemas de Administracion de datos
# Proyecto Final
# Sistema de Informacion Empresarial de Uñas con tecnologia Wireless 

CREATE DATABASE if not exists proyecto_final; 

USE proyecto_final;

CREATE TABLE empleados (
	empleado_id INT NOT NULL AUTO_INCREMENT,
    emp_nombre VARCHAR(50) NOT NULL,
    emp_fecha_nac DATE NOT NULL,
    emp_cargo VARCHAR(30) NOT NULL,
    emp_salario DECIMAL(10,2) NOT NULL,
    emp_fecha_contratacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    emp_telefono VARCHAR(10) NOT NULL, 
    emp_correo VARCHAR( 45),
    UNIQUE (emp_telefono),
    INDEX idx_emp_nombre(emp_nombre),
    PRIMARY KEY(empleado_id)
);
CREATE TABLE asistencia (
	asistencia_id INT NOT NULL AUTO_INCREMENT,
    empleado_id INT,
	asi_registro ENUM('Entrada','Salida'),
    asi_hora_salida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    asi_estado ENUM('A tiempo','Retardo'),
    PRIMARY KEY(asistencia_id),
    CONSTRAINT fk_empleado FOREIGN KEY (empleado_id) REFERENCES empleados(empleado_id)
);
CREATE TABLE clientes (
	cliente_id INT NOT NULL AUTO_INCREMENT,
    cli_nombre VARCHAR(50) NOT NULL, 
    cli_correo VARCHAR(50) NOT NULL,
    cli_telefono VARCHAR(10) NOT NULL,
    UNIQUE(cli_nombre),
    INDEX idx_cli_telefono(cli_telefono),
    PRIMARY KEY(cliente_id)
);
CREATE TABLE direcciones(
	direcciones_id INT NOT NULL AUTO_INCREMENT,
    cliente_id  INT NOT NULL,
    dir_direccion VARCHAR(50) NOT NULL,
    dir_ciudad VARCHAR(25) NOT NULL,
    dir_codigo_postal VARCHAR(15) NOT NULL, 
    dir_pais VARCHAR(35) NOT NULL,
    PRIMARY KEY(direcciones_id),
    CONSTRAINT fk_clientes FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
);
CREATE TABLE producto(
	producto_id INT NOT NULL AUTO_INCREMENT,
    pro_nombre ENUM('NavyBlue','RedCherry','PearlWhite','OceanBlack'),
    pro_tamaño ENUM('Chico','Mediano','Grande'),
    pro_fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pro_precio decimal(10,2) NOT NULL,
    pro_estado ENUM('Activo','Inactivo') NOT NULL,
    PRIMARY KEY(producto_id)
);
CREATE TABLE pedidos(
	pedido_id INT NOT NULL AUTO_INCREMENT,
    cliente_id INT,
    direcciones_id INT, 
    ped_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ped_notas TEXT,
    ped_metodo_pago ENUM('Tarjeta Credito/Debito','Paypal','Efectivo en puntos de pago'),
    PRIMARY KEY(pedido_id),
    CONSTRAINT fk_direcciones FOREIGN KEY (direcciones_id) REFERENCES direcciones(direcciones_id),
    CONSTRAINT fk_clientes_3 FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
);
CREATE TABLE detalle_pedido(
	detalle_id INT NOT NULL AUTO_INCREMENT,
    pedido_id INT,
    producto_id INT,
    det_cantidad INT NOT NULL,
    det_precio_total DECIMAL(10,2) NOT NULL,
    PRIMARY KEY(detalle_id),
    CONSTRAINT fk_pedidos_1 FOREIGN KEY (pedido_id) REFERENCES pedidos(pedido_id),
    CONSTRAINT fk_producto_5 FOREIGN KEY (producto_id) REFERENCES producto(producto_id)
);
CREATE TABLE envios (
	envio_id INT NOT NULL AUTO_INCREMENT,
    pedido_id INT,
    cliente_id INT, 
    env_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    env_estado ENUM('Entregado','En transito','Por enviar'),
    env_metodo_envio ENUM('Estandar','Express'),
    env_seguimiento VARCHAR(20) NOT NULL,
    env_costo_envio DECIMAL(10,2) NOT NULL,
    PRIMARY KEY(envio_id),
    CONSTRAINT fk_pedidos_9 FOREIGN KEY (pedido_id) REFERENCES pedidos(pedido_id),
    CONSTRAINT fk_clientes_1 FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
);
CREATE TABLE material(
	material_id INT NOT NULL AUTO_INCREMENT,
    mat_nombre VARCHAR(40) NOT NULL,
    mat_descripcion TEXT NOT NULL, 
    PRIMARY KEY(material_id)
);
CREATE TABLE almacenes(
	almacen_id INT NOT NULL AUTO_INCREMENT,
    alm_nombre VARCHAR(50) NOT NULL, 
    alm_ubicacion VARCHAR(50) NOT NULL,
    PRIMARY KEY(almacen_id)
);
CREATE TABLE proveedores(
	proveedor_id INT NOT NULL AUTO_INCREMENT,
    material_id INT, 
    prov_nombre VARCHAR(25) NOT NULL, 
    prov_contacto VARCHAR(25), 
	prov_telefono VARCHAR(10) NOT NULL,
    prov_correo VARCHAR(50),
    prov_direccion VARCHAR(50) NOT NULL,
    PRIMARY KEY(proveedor_id),
    CONSTRAINT fk_material_1 FOREIGN KEY (material_id) REFERENCES material(material_id)
);
CREATE TABLE inventario_productos(
	inventario_productos_id INT NOT NULL AUTO_INCREMENT,
    almacen_id INT NOT NULL,
    producto_id INT,
    inv_cantidad INT NOT NULL,-- cantidad actual
    inv_ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (inventario_productos_id),
    CONSTRAINT fk_almacen_1 FOREIGN KEY (almacen_id) REFERENCES almacenes(almacen_id),
    CONSTRAINT fk_producto_3 FOREIGN KEY (producto_id) REFERENCES producto(producto_id)
);
CREATE TABLE movimientos_inv_productos(
    movimiento_id INT NOT NULL AUTO_INCREMENT,
    inventario_productos_id INT NOT NULL,          -- Relación con inventario
    mov_tipo_movimiento ENUM('Entrada', 'Salida') NOT NULL,
    mov_cantidad INT NOT NULL,
    mov_fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mov_descripcion VARCHAR(255),           -- Detalles del movimiento
    PRIMARY KEY (movimiento_id),
    CONSTRAINT fk_inventario_productos FOREIGN KEY (inventario_productos_id) REFERENCES inventario_productos(inventario_productos_id)
);
CREATE TABLE inventario_materiales(
	inventario_materiales_id INT NOT NULL AUTO_INCREMENT,
    almacen_id INT NOT NULL,
    material_id INT NOT NULL,
    inv_cantidad INT NOT NULL,
    inv_mat_ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (inventario_materiales_id),
    CONSTRAINT fk_almacen_2 FOREIGN KEY (almacen_id) REFERENCES almacenes(almacen_id),
    CONSTRAINT fk_material_2 FOREIGN KEY (material_id) REFERENCES material(material_id)
);
CREATE TABLE movimientos_inv_materiales(
    movimiento_inv_materiales_id INT NOT NULL AUTO_INCREMENT,
    inventario_materiales_id INT NOT NULL,          -- Relación con inventario
    mov_pro_tipo_movimiento ENUM('Entrada', 'Salida') NOT NULL,
    mov_pro_cantidad INT NOT NULL,
    mov_pro_fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mov_pro_descripcion VARCHAR(255),           -- Detalles del movimiento
    PRIMARY KEY (movimiento_inv_materiales_id),
    CONSTRAINT fk_inventario_materiales FOREIGN KEY (inventario_materiales_id) REFERENCES inventario_materiales(inventario_materiales_id)
);




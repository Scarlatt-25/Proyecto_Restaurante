CREATE SEQUENCE seq_clientes START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_productos START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_pedidos START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_pedidos_items START WITH 1 INCREMENT BY 1;

CREATE TABLE clientes (
    cliente_id NUMBER PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    telefono VARCHAR2(20),
    direccion VARCHAR2(200),
    email VARCHAR2(100)
);

CREATE TABLE productos (
    productos_id NUMBER PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(255),
    precio NUMBER(10,2),
    disponible CHAR(1) DEFAULT 'S' CHECK (disponible IN ('S','N'))
);

CREATE TABLE pedidos (
    pedido_id NUMBER PRIMARY KEY,
    tipo VARCHAR2(30) NOT NULL,
    cliente_id NUMBER,
    fecha DATE DEFAULT SYSDATE,
    total NUMBER(10,2),
    mesa VARCHAR2(10),
    tiempo_estimado NUMBER,
    direccion_entrega VARCHAR2(100),
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
);

CREATE TABLE pedido_items (
    item_id NUMBER FOREIGN KEY,
    pedido_id NUMBER NOT NULL,
    productos_id NUMBER NOT NULL,
    cantidad NUMBER(5) DEFAULT 1,
    precio_unit NUMBER (10,2),
    subtotal NUMBER(10,2),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(pedido_id),
    FOREIGN KEY (productos_id) REFERENCES productos(productos_id)
);

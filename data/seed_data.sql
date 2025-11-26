
-- Cientes
INSERT INTO clientes(nombre, telefono, direccion, email)VALUES('Catalina Maldonado','+56912345678','Av. Siempre Viva 123','catalina@mail.cl');
INSERT INTO clientes(nombre, telefono, direccion, email)VALUES('Javier Herrera','+56987654321','Calle False 45','javier@mail.cl');
 
-- Productos
INSERT INTO productos(productos_id, nombre, descripcion, precio, disponible)VALUES(seq_productos.NEXTVAL,'Pizza Margarita','Base tomate, queso, albahaca',7000,'S');
INSERT INTO productos(productos_id, nombre, descripcion, precio, disponible)VALUES(seq_productos.NEXTVAL,'Empanada de Pino','Rellena de carne',1200,'S');
INSERT INTO productos(productos_id, nombre, descripcion, precio, disponible)VALUES(seq_productos.NEXTVAL,'Ensalada César','Lechuga, pollo, aderezo',5000,'S');

-- Pedidos de ejemplo (pedidos vacios, items se insertan después)
INSERT INTO pedidos(pedido_id, tipo, cliente_id, fecha, total, mesa, tiempo_estimado)VALUES(seq_pedidos.NEXTVAL,'local',1, SYSDATE,0,'A1',20);
INSERT INTO pedidos(pedido_id, tipo, cliente_id, fecha, total, direccion_entrega, repartidor)VALUES(seq_pedidos.NEXTVAL, 'domicilio',2, SYSDATE,0,'Calle Falsa 45','Pedro repartidor');

-- Items ejemplo (si quieres)
INSERT INTO pedido_items(item_id, pedido_id,productos_id, cantidad, precio_unit, subtotal)VALUES(seq_pedidos_items.NEXTVAL,1,1,1,7000,7000);
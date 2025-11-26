from src import db
from src.exceptions import NotFoundError, DatabaseError
from src.models import Cliente, Producto, PedidoLocal, PedidoParaLlevar, PedidoADomicilio
import oracledb

def crear_cliente(cliente: Cliente):
    sql = """
    INSERT INTO clientes(cliente_id, nombre, telefono, direccion, email)VALUES(seq_clientes.NEXTVAL, :nombre, :telefono, :direccion, :email) """
    
    try:
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, {
                    "nombre": cliente.nombre,
                    "telefono": cliente._telefono,
                    "direccion": cliente._direccion,
                    "email": cliente._email
                })

                cur.execute("SELECT seq_clientes.CURRVAL FROM dual")
                cliente_id = cur.fetchone()[0]
                conn.commit()
                cliente.cliente_id = cliente_id
                return cliente_id
    except oracledb.DatabaseError as e:
        raise DatabaseError(str(e))
    
def listar_clientes():
    return db.fetch_all("SELECT cliente_id, nombre, telefono, direccion,email FROM clientes ORDEN BY cliente_id")

def obtener_cliente(cliente_id):
    rows = db.fetch_all("SELECT cliente_id, nombre, telefono, direccion,email FROM clientes WHERE cliente_id = :id", {"id": cliente_id})
    if not rows:
        raise NotFoundError("Cliente no encontrado")
    r =rows[0]
    return Cliente(nombre=r['nombre'], telefono=r['telefono'], direccion=r['direccion'], email=r['email'], cliente_id=r['cliente_id'])

def actualizar_cliente(cliente: Cliente):
    sql = """
    UPDATE clientes
    SET nombre = :nombre, telefono = :telefono, direccion = :direccion, email = :email
    WHERE cliente_id = :id
    """
    try:
        return db.execute(sql,{"nombre": cliente.nombre, "telefono": cliente._telefono, "direccion": cliente._direccion, "email": cliente._email, "id": cliente._cliente_id})
    except oracledb.DatabaseError as e:
        raise DatabaseError(str(e))
    
def eliminar_cliente(cliente_id):
    try:
        return db.execute("DELETE FROM clientes WHERE cliente_id = :id", {"id": cliente_id})
    except oracledb.DatabaseError as e:
        raise DatabaseError(str(e))
    
def crear_producto(producto: Producto):
    sql = """
    INSERT INTO productos(producto_id, nombre, decripcion, precio, disponible)VALUES(seq_productos.NEXTVAL, :nombre, :descripcion, :precio, :disponible)"""

    try:
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, {
                    "nombre": producto._nombre,
                    "descripcion": producto._descripcion,
                    "precio": producto._precio,
                    "disponible": producto._disponible
                })
                cur.execute(("SELECT seq_producto.CURRVAL FROM dual"))
                pid = cur.fetchone()[0]
                conn.commit()
                producto._producto_id = pid
                return pid
    except oracledb.DatabaseError as e:
        raise DatabaseError(str(e))
    
def listar_producto():
    return db.fetch_all("SELECT producto_id, nombre, descripcion, precio, disponible FROM productos ORDEN BY producto_id")

def obtener_producto(producto_id):
    rows = db.fetch_all("SELECT producto_id, nombre, descripcion, precio, disponible FROM productos WHERE producto_id = :id", {"id": producto_id})
    if not rows:
        raise NotFoundError("Producto no encontrado")
    r = rows[0]
    return Producto(nombre=r['nombre'], precio=r['precio'], descripcion=r['descripcion'], disponible=r['disponible'], producto_id=r['producto_id'])

def actualizar_producto(producto: Producto):
    sql = """
    UPDATE producto SET nombre = :nombre, descripcion = :descripcion, precio = :precio, disponible = :disponible
    WHERE producto_id = :id
    """
    try:
        return db.execute(sql, {"nombre": producto._nombre, "descripcion": producto._descripcion, "precio": producto._precio, "disponible": producto._disponible, "id": producto._producto_id})
    
    except oracledb.DatabaseError as e:
        raise DatabaseError(str(e))
    
def eliminar_producto(producto_id):
    try:
        return db.execute("DELETE FROM productos WHERE producto_id = :id",{"id": producto_id})
    except oracledb.DatabaseError as e:
        raise DatabaseError(str(e))
    

def crear_pedido(pedido: PedidoLocal or PedidoParaLlevar or PedidoADomicilio): # type: ignore
    try:
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                # Insert pedido principal con NEXTVAL y luego recuperar currval
                insert_pedido_sql = """
                INSERT INTO pedidos(pedido_id, tipo, cliente_id, fecha, total, mesa, tiempo_estimado, direccion_entrega, repartidor)
                VALUES (seq_pedidos.NEXTVAL, :tipo, :cliente_id, :fecha, :total, :mesa, :tiempo_estimado, :direccion_entrega, :repartidor)
                """
                tipo = pedido.to_dict().get("tipo")
                d = pedido.to_dict()
                cur.execute(insert_pedido_sql, {
                    "tipo": tipo,
                    "cliente_id": d.get("cliente_id"),
                    "fecha": d.get("fecha"),
                    "total": d.get("total"),
                    "mesa": d.get("mesa"),
                    "tiempo_estimado": d.get("tiempo_estimado"),
                    "direccion_entrega": d.get("direccion_entrega"),
                    "repartidor": d.get("repartidor")
                })
                cur.execute("SELECT seq_pedidos.CURRVAL FROM dual")
                pedido_id = cur.fetchone()[0]
                # Insert items
                for item in d.get("items", []):
                    cur.execute("""
                        INSERT INTO pedido_items(item_id, pedido_id, producto_id, cantidad, precio_unit, subtotal)
                        VALUES (seq_pedido_items.NEXTVAL, :pedido_id, :producto_id, :cantidad, :precio_unit, :subtotal)
                    """, {
                        "pedido_id": pedido_id,
                        "producto_id": item['producto_id'],
                        "cantidad": item['cantidad'],
                        "precio_unit": item['precio_unit'],
                        "subtotal": item['subtotal']
                    })
                # actualizar total
                cur.execute("UPDATE pedidos SET total = :total WHERE pedido_id = :id", {"total": d.get("total"), "id": pedido_id})
                conn.commit()
                pedido.pedido_id = pedido_id
                return pedido_id
    except oracledb.DatabaseError as e:
        raise DatabaseError(str(e))

def listar_pedidos():
    sql = """
    SELECT p.pedido_id, p.tipo, p.cliente_id, p.fecha, p.total, p.mesa, p.tiempo_estimado, p.direccion_entrega, p.repartidor
    FROM pedidos p
    ORDER BY p.pedido_id
    """
    return db.fetch_all(sql)

def obtener_pedido(pedido_id):
    sql = "SELECT pedido_id, tipo, cliente_id, fecha, total, mesa, tiempo_estimado, direccion_entrega, repartidor FROM pedidos WHERE pedido_id = :id"
    rows = db.fetch_all(sql, {"id": pedido_id})
    if not rows:
        raise NotFoundError("Pedido no encontrado")
    p = rows[0]
    items = db.fetch_all("SELECT item_id, producto_id, cantidad, precio_unit, subtotal FROM pedido_items WHERE pedido_id = :id", {"id": pedido_id})
    p['items'] = items
    return p

def eliminar_pedido(pedido_id):
    try:
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM pedido_items WHERE pedido_id = :id", {"id": pedido_id})
                cur.execute("DELETE FROM pedidos WHERE pedido_id = :id", {"id": pedido_id})
                conn.commit()
                return True
    except oracledb.DatabaseError as e:
        raise DatabaseError(str(e))
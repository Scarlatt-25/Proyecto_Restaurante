# src/cli.py
import sys
from tabulate import tabulate
from src import crud
from src.models import Cliente, Producto, PedidoLocal, PedidoParaLlevar, PedidoADomicilio
from src.exceptions import NotFoundError, ValidationError
import traceback

def pause():
    input("\nEnter para volver al menú...")

def mostrar_tabla(rows, headers=None):
    if not rows:
        print("— vacío —")
        return
    print(tabulate(rows, headers="keys", tablefmt="psql"))

def menu_principal():
    while True:
        print("\n=== Sistema Restaurante (OracleDB) ===")
        print("1) Clientes - Listar")
        print("2) Clientes - Crear")
        print("3) Productos - Listar")
        print("4) Productos - Crear")
        print("5) Pedidos - Listar")
        print("6) Crear Pedido (ejemplo)")
        print("7) Ver Pedido (por id)")
        print("8) Eliminar Pedido")
        print("0) Salir")
        opt = input("Elige opción: ").strip()
        try:
            if opt == "1":
                rows = crud.listar_clientes()
                mostrar_tabla(rows)
                pause()
            elif opt == "2":
                nombre = input("Nombre: ").strip()
                telefono = input("Teléfono: ").strip()
                direccion = input("Dirección: ").strip()
                email = input("Email: ").strip()
                c = Cliente(nombre=nombre, telefono=telefono, direccion=direccion, email=email)
                cid = crud.crear_cliente(c)
                print(f"Cliente creado con id {cid}")
                pause()
            elif opt == "3":
                rows = crud.listar_productos()
                mostrar_tabla(rows)
                pause()
            elif opt == "4":
                nombre = input("Nombre producto: ").strip()
                desc = input("Descripción: ").strip()
                precio = float(input("Precio: ").strip())
                prod = Producto(nombre=nombre, precio=precio, descripcion=desc)
                pid = crud.crear_producto(prod)
                print(f"Producto creado con id {pid}")
                pause()
            elif opt == "5":
                rows = crud.listar_pedidos()
                mostrar_tabla(rows)
                pause()
            elif opt == "6":
                crear_pedido_interactivo()
            elif opt == "7":
                pid = int(input("ID pedido: ").strip())
                p = crud.obtener_pedido(pid)
                mostrar_tabla(p.get("items", []))
                print("\nMeta:", {k:v for k,v in p.items() if k != "items"})
                pause()
            elif opt == "8":
                pid = int(input("ID pedido a eliminar: ").strip())
                crud.eliminar_pedido(pid)
                print("Pedido eliminado.")
                pause()
            elif opt == "0":
                print("Chao! 👍")
                sys.exit(0)
            else:
                print("Opción inválida")
        except Exception as e:
            print("Ocurrió un error:", str(e))
            traceback.print_exc()
            pause()

def crear_pedido_interactivo():
    print("\nTipos de pedido: 1) Local  2) Para llevar  3) Domicilio")
    t = input("Elige tipo: ").strip()
    cliente_id = int(input("Cliente ID (usar listar clientes para ver ids): ").strip())
    if t == "1":
        mesa = input("Mesa (ej A1): ").strip()
        tiempo = int(input("Tiempo estimado (min): ").strip() or 20)
        pedido = PedidoLocal(mesa=mesa, tiempo_estimado=tiempo, cliente_id=cliente_id)
    elif t == "2":
        tiempo = int(input("Tiempo estimado (min): ").strip() or 25)
        pedido = PedidoParaLlevar(tiempo_estimado=tiempo, cliente_id=cliente_id)
    elif t == "3":
        direccion = input("Dirección entrega: ").strip()
        repartidor = input("Nombre repartidor (opcional): ").strip() or None
        pedido = PedidoADomicilio(direccion_entrega=direccion, repartidor=repartidor, cliente_id=cliente_id)
    else:
        print("Tipo inválido")
        return

    # añadir items
    print("Agrega items (producto_id,cantidad). escribe 'fin' para terminar.")
    while True:
        linea = input("producto_id,cantidad: ").strip()
        if linea.lower() in ("fin","f","salir"):
            break
        try:
            pid_str, qty_str = linea.split(",")
            pid = int(pid_str.strip()); qty = int(qty_str.strip())
            prod = crud.obtener_producto(pid)
            precio = prod._precio if hasattr(prod, "_precio") else prod['precio']
            pedido.add_item(producto_id=pid, cantidad=qty, precio_unit=precio)
            print(f"Agregado: producto {pid} x{qty}")
        except Exception as e:
            print("Error al agregar item:", e)

    print("Procesando pedido:", pedido.procesar())
    pid = crud.crear_pedido(pedido)
    print(f"Pedido creado con id {pid}")
    pause()

if __name__ == "__main__":
    menu_principal()

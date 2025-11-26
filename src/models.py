from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, nombre, telefono=None, direccion=None, email=None, cliente_id=None):
        self._cliente_id = cliente_id
        self._nombre = nombre
        self._telefono = telefono
        self._direccion = direccion
        self._email = email

    @property
    def cliente_id(self):
        return self._cliente_id
    
    @cliente_id.setter
    def cliente_id(self, value):
        self._cliente_id = value

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        if not value:
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = value

    def to_dict(self):
        return {
            "cliente_id": self._cliente_id,
            "nombre": self._nombre,
            "telefono": self._telefono,
            "direccion": self._direccion,
            "email": self._email
        }
    
class Producto:
    def __init__(self, nombre, precio, descripcion=None, disponible='S', producto_id=None):
        self._producto_id = producto_id
        self._nombre = nombre
        self._descripcion = descripcion
        self._precio = precio
        self._disponible = disponible

    @property
    def producto_id(self):
        return self._producto_id
    
    def to_dict(self):
        return{
            "producto_id": self._producto_id,
            "nombre": self._nombre,
            "descripcion": self._descripcion,
            "precio": self._precio,
            "disponible": self._disponible
        }
    
class Pedido(ABC):
    def __init__(self, cliente_id=None, fecha=None, total=0.0, pedido_id=None):
        self._pedido_id = pedido_id
        self._cliente_id = cliente_id
        self._fecha = fecha
        self._total = float(total)
        self._items = []

    @property
    def pedido_id(self):
        return self._pedido_id
    
    @pedido_id.setter
    def pedido_id(self, value):
        self._pedido_id = value

    @property
    def total(self):
        return self._total
    
    def add_item(self, producto_id, cantidad, precio_unit):
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor a 0")
        subtotal = cantidad * float(precio_unit)
        self._items.append({
            "producto_id": producto_id,
            "cantidad": cantidad,
            "precio_unit":float(precio_unit),
            "subtotal": subtotal
        })
        self._recalculate_total()
    
    def _recalculate_total(self):
        self._total = sum(i['subtotal'] for i in self._items)

    @abstractmethod

    def procesar(self):
        """Método polimórfico: comportamiento distinto según tipo."""
        pass

    def to_dict_common(self):
        return {
            "pedido_id": self._pedido_id,
            "cliente_id": self._cliente_id,
            "fecha": self._fecha,
            "total": self._total,
            "items": self._items
        }
    
class PedidoLocal(Pedido):
    def __init__(self, mesa, tiempo_estimado=30,**kwargs):
        super().__init__(**kwargs)
        self._mesa = mesa
        self._tiempo_estimado = tiempo_estimado

    def procesar(self):
        return f"Pedido local para mesa {self._mesa}. Tiempo estimado {self._tiempo_estimado} minutos."
    
    def to_dict(self):
        d = self.to_dict_common()
        d.update({"tipo": "LOCAL", "mesa": self._mesa, "tiempo_estimado": self._tiempo_estimado})
        return d

class PedidoParaLlevar(Pedido):
    def __init__(self, tiempo_estimado=25, **kwargs):
        super().__init__(**kwargs)
        self._tiempo_estimado = tiempo_estimado

    def procesar(self):
        return f"Pedido para llevar. Tiempo estimado {self._tiempo_estimado} minutos."
    
    def to_dict(self):
        d = self.to_dict_common()
        d.update({"tipo": "LLEVAR", "tiempo_estimado": self._tiempo_estimado})
        return d

class PedidoADomicilio(Pedido):
    def __init__(self, tiempo_estimado=25, **kwargs):
        super().__init__(**kwargs)
        self._tiempo_estimado = tiempo_estimado

    def procesar(self):
        rp = self._repartidor or "sin repartidor asignado"
        return f"Pedido a domicilio a {self._direccion_entrega}. Repartidor: {rp}."
    
    def to_dict(self):
        d = self.to_dict_common()
        d.update({"tipo": "DOMICILIO", "direccion_entrega: self._direccion_entrega": self._direccion_entrega, "repartidor": self._repartidor})
        return d


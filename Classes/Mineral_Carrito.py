class MineralCarrito:

    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad,
            'total': self.calcular_total()
        }
    
    def __repr__(self):
        return f"MineralCarrito('{self.nombre}', '{self.precio}', '{self.cantidad}')"

    def actualizar_cantidad(self, nueva_cantidad):
        self.cantidad = nueva_cantidad

    def calcular_total(self):
        return self.precio * self.cantidad

    def incrementar_cantidad(self, incremento=1):
        self.cantidad += incremento

    def decrementar_cantidad(self, decremento=1):
        if self.cantidad - decremento >= 0:
            self.cantidad -= decremento

    def calcular_total(self):
        return self.precio * self.cantidad
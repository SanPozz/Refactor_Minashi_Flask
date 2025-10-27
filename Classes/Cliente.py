class Cliente(Usuario):
    def __init__(self, username, mail, password, rol, id_cliente, direccion):
        super().__init__(username, mail, password, rol)
        self.id_cliente = id_cliente
        self.direccion = direccion

    def mostrar_informacion(self):
        info_usuario = super().mostrar_informacion()
        return f"{info_usuario}, ID Cliente: {self.id_cliente}, Dirección: {self.direccion}"
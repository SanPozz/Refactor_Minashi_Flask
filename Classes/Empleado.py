class Empleado(Usuario):
    def __init__(self, username, mail, password, rol, id_empleado, cargo):
        super().__init__(username, mail, password, rol)
        self.id_empleado = id_empleado
        self.cargo = cargo

    def mostrar_informacion(self):
        info_usuario = super().mostrar_informacion()
        return f"{info_usuario}, ID Empleado: {self.id_empleado}, Cargo: {self.cargo}"
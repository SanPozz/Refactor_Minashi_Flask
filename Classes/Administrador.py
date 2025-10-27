from Classes.Usuario import Usuario

class Administrador(Usuario):
    def __init__(self, username, mail, password, rol, id_admin):
        super().__init__(username, mail, password, rol)
        self.id_admin = id_admin

    def mostrar_informacion(self):
        info_usuario = super().mostrar_informacion()
        return f"{info_usuario}, ID Administrador: {self.id_admin}"
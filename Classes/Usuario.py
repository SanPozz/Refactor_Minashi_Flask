class Usuario:
    def __init__ (self, username, mail, password, rol):
        self.username = username
        self.mail = mail
        self.password = password
        self.rol = rol
    
    def to_dict(self):
        return {
            'username': self.username,
            'mail': self.mail,
            'password': self.password,
            'rol': self.rol
        }
    
    def __repr__(self):
        return f"Usuario('{self.username}', '{self.mail}', '{self.password}', '{self.rol}')"
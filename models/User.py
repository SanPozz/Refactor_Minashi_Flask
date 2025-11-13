from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users' 
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    mail = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.String(50), default='user')


    def __repr__(self):
        return f"User('{self.username}')"
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'mail': self.mail,
            'role': self.role
        }

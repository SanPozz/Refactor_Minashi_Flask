from database import db

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pendiente')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    items = db.relationship('PedidoItem', backref='pedido', lazy=True)

    def __repr__(self):
        return f"Pedido('{self.id}', '{self.user_id}', '{self.total_price}', '{self.status}')"
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_price': self.total_price,
            'status': self.status,
            'created_at': self.created_at
        }
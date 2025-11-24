from database import db

class PedidoItem(db.Model):
    __tablename__ = 'pedido_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    mineral = db.Column(db.String(150), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)


    def __repr__(self):
        return f"PedidoItem('{self.mineral}', '{self.cantidad}', '{self.precio_unitario}')"
    
    def to_dict(self):
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'mineral': self.mineral,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario
        }
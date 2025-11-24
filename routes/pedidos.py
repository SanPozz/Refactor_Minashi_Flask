from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models.Pedido import Pedido

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/mis_pedidos', methods=['GET'])
@login_required
def mis_pedidos():

    user = current_user

    pedidos = Pedido.query.filter_by(user_id=user.id).all()
    
    return render_template('mis_pedidos.html', pedidos=pedidos)

@pedidos_bp.route('/ver_detalles_pedido/<int:pedido_id>', methods=['GET'])
@login_required
def ver_detalles_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    return render_template('detalle_pedido.html', pedido=pedido)
from flask import Blueprint, render_template, request, redirect, url_for

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/mis_pedidos', methods=['GET'])
def mis_pedidos():
    
    return render_template('mis_pedidos.html')

from flask import Blueprint, render_template, request, redirect, url_for

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/ver_pedidos', methods=['GET'])
def ver_pedidos():
    
    return render_template('ver_pedidos.html')

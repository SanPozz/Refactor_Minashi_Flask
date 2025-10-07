from flask import Blueprint, render_template, request, redirect, url_for

venta_minerales_bp = Blueprint('venta_minerales', __name__)

@venta_minerales_bp.route('/comprar_minerales')
def comprar_minerales():
    
    return render_template('comprar_minerales.html')

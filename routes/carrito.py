from flask import Blueprint, render_template, request, redirect, url_for

carrito_bp = Blueprint('carrito', __name__)

@carrito_bp.route('/carrito', methods=['GET', 'POST'])
def carrito():

    return render_template('carrito.html')
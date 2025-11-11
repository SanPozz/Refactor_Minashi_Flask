from flask import Blueprint, render_template, request, redirect, session, url_for

from Classes.Mineral_Carrito import MineralCarrito

carrito_bp = Blueprint('carrito', __name__)

@carrito_bp.route('/carrito', methods=['GET', 'POST'])
def ver_carrito():

    cart = session.get('cart', [])

    for item in cart:
        print(item)

    return render_template('mi_carrito.html', cart=cart)

@carrito_bp.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():

    if request.method == 'POST':
        metal = request.form['metal']
        precio = float(request.form['precio'])
        cantidad = int(request.form['cantidad'])

        cart = session.get('cart', [])

        prod = MineralCarrito(metal, precio, cantidad)

        existe = False;

        for item in cart:
            for key, value in item.items():
                if key == 'nombre':
                    if value == metal:
                        existe = True
                        item['cantidad'] += cantidad
                        item['total'] = item['cantidad'] * item['precio']
                        break

        if existe == False:
            cart.append(prod.to_dict())

        session['cart'] = cart
        session.modified = True

        return redirect(url_for('venta_minerales.comprar_minerales', resultado='agregado'))
    
@carrito_bp.route('/vaciar_carrito')
def vaciar_carrito():
        session['cart'] = []
        session.modified = True
        return redirect(url_for('carrito.ver_carrito'))
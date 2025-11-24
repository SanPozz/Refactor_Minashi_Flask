from flask import Blueprint, render_template, request, redirect, session, url_for
from models.Pedido import Pedido
from models.PedidoItem import PedidoItem
from Classes.Mineral_Carrito import MineralCarrito
from flask_login import login_required, current_user
from database import db

carrito_bp = Blueprint('carrito', __name__)

@carrito_bp.route('/carrito', methods=['GET', 'POST'])
def ver_carrito():

    cart = session.get('cart', [])
    total = 0
    for item in cart:
        total += item['total']
        
    return render_template('mi_carrito.html', cart=cart, total=total)

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

@carrito_bp.route('/eliminar_del_carrito/<string:metal>')
def eliminar_del_carrito(metal):
        cart = session.get('cart', [])
        cart = [item for item in cart if item['nombre'] != metal]
        session['cart'] = cart
        session.modified = True
        return redirect(url_for('carrito.ver_carrito'))

@carrito_bp.route('/finalizar_compra')
def finalizar_compra():
        
        cart = session.get('cart', [])

        if not cart:
            return redirect(url_for('carrito.ver_carrito'))

        user_id = current_user.id
        
        pedido = Pedido(user_id=user_id, total_price=sum(item['total'] for item in cart), status='pendiente')

        pedido.items = []

        for item in cart:
            pedido_item = PedidoItem(
                pedido_id=pedido,
                mineral=item['nombre'],
                precio_unitario=item['precio'],
                cantidad=item['cantidad'],
            )
            pedido.items.append(pedido_item)

        db.session.add(pedido)
        db.session.commit()


        session['cart'] = []
        session.modified = True
        return redirect(url_for('venta_minerales.comprar_minerales', resultado='compra_exitosa'))


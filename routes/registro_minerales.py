from flask import Blueprint, render_template, request, redirect, url_for,Response,flash
from dotenv import load_dotenv;
import os,json;
from flask import current_app
import requests;
from models.Mineral import Mineral
from models.User import User
from database import db
import pandas as pd
from datetime import datetime

load_dotenv();

API_KEY = os.getenv('API_KEY');
URL_API = os.getenv('URL_API');


registro_minerales_bp = Blueprint('registro_minerales', __name__)



@registro_minerales_bp.route('/registro_mineral', methods=['GET', 'POST'])
def registrar_minerales():

    # url = f"{URL_API}?api_key={API_KEY}&unit=kg&currency=ARS"

    headers = {}

    headers["Accept"] = "application/json"

    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        description = request.form.get('description')
        
        if not name or not price or not stock:
            return render_template('registro_mineral.html', error='Todos los campos son obligatorios')
        
        if Mineral.query.filter_by(name=name).first():
            return render_template('registro_mineral.html', error='El mineral ya está registrado')
        
        try:
            mineral_nuevo = Mineral(
                name=name,
                price=float(price),
                stock=int(stock),
                description=description if description else 'No description available'
            )
            db.session.add(mineral_nuevo)
            db.session.commit()
            
            return redirect(url_for('registro_minerales.ver_stock'))
        except Exception as e:
            db.session.rollback()
            return render_template('registro_mineral.html', error='Error al registrar el mineral en la base de datos')

    return render_template('registro_mineral.html')





@registro_minerales_bp.route('/ver_stock')
def ver_stock():
    data = load_json_from_file()
    metals = data.get('metals', {})
    currency = data.get('currency', 'ARS')

    minerales_db = Mineral.query.all()


    minerales_completos = []
    nombres_procesados = []

    for mineral in minerales_db:

            minerales_completos.append({
                'id': mineral.id,
                'name': mineral.name,
                'price': mineral.price,
                'description': mineral.description,
                'stock': mineral.stock,
                'es_base': True

            })

    for nombre_metal, precio in metals.items():
        if nombre_metal not in nombres_procesados:
            minerales_completos.append({
                'id': '-',
                'name': nombre_metal,
                'price': precio,
                'description': 'Mineral externo (JSON)',
                'stock': '-',
                'image_url': '', 
                'es_base': False 
            })


    print("Precio Minerales:", minerales_completos)

    return render_template('ver_stock.html', minerales=minerales_completos, currency=currency)


@registro_minerales_bp.route('/editar_mineral/<nombre>', methods=['GET', 'POST'])
def editar_mineral(nombre):
    
    mineral = Mineral.query.filter_by(name=nombre).first()

    
    if not mineral:
        return redirect(url_for('registro_minerales.ver_stock'))

    if request.method == 'POST':
       
        nuevo_nombre = request.form.get('name')
        nuevo_precio = request.form.get('price')
        nuevo_stock = request.form.get('stock')
        nueva_descripcion = request.form.get('description')

        try:
            
            mineral.name = nuevo_nombre
            mineral.price = float(nuevo_precio)
            mineral.stock = int(nuevo_stock)
            mineral.description = nueva_descripcion
            
            
            db.session.commit()
            return redirect(url_for('registro_minerales.ver_stock'))
            
        except Exception as e:
            db.session.rollback()
            return render_template('editar_mineral.html', mineral=mineral, error="Error al actualizar")

    
    return render_template('editar_mineral.html', mineral=mineral)

@registro_minerales_bp.route('/eliminar_mineral/<nombre>', methods=['POST'])
def eliminar_mineral(nombre):

    mineral = Mineral.query.filter_by(name=nombre).first()

    if mineral:
        try:
            db.session.delete(mineral)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    
    return redirect(url_for('registro_minerales.ver_stock'))


@registro_minerales_bp.route('/usuarios')
def usuarios():
    users = User.query.all()
    return render_template('usuarios.html', users=users)


@registro_minerales_bp.route('/exportar_csv', methods=['GET'])
def exportar_csv():
   
    section = request.args.get('page', '')
    df = None 

    if section not in ['usuarios', 'minerales']:
        return redirect(url_for('registro_minerales.ver_stock'))
    
    if section == 'usuarios':
        users = User.query.all()
        data = [{'ID': user.id, 'Nombre': user.username, 'Email': user.mail, 'Role': user.role} for user in users]
        df = pd.DataFrame(data)

    elif section == 'minerales':
        
        url = f"{URL_API}?api_key={API_KEY}&unit=kg&currency=ARS"
        headers = {"Accept": "application/json"}
        
        try:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status() 
            data = resp.json()
            
            metalsRaw = data.get('metals', {})
            data_list = [{'Mineral': metal, 'Precio': precio} for metal, precio in metalsRaw.items()]
            df = pd.DataFrame(data_list)
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error al obtener datos de la API para exportar minerales: {e}")
            return Response("Error al obtener datos de minerales para exportar.", status=500)

    if df is not None:
        csv_data = df.to_csv(index=False)
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment;filename={section}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            }
        )
    
    return redirect(url_for('registro_minerales.ver_stock')) 

@registro_minerales_bp.route('/editar_rol/<int:user_id>', methods=['POST'])
def editar_rol_usuario(user_id):
    user_to_edit = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    allowed_roles = ['user', 'admin']
    if new_role not in allowed_roles:
        flash('Rol no válido.', 'error')
        return redirect(url_for('registro_minerales.usuarios'))
    user_to_edit.role = new_role
    db.session.commit()
    flash('Rol actualizado con éxito.', 'success')
    return redirect(url_for('registro_minerales.usuarios'))

@registro_minerales_bp.route('/eliminar_usuario/<int:user_id>', methods=['POST'])
def eliminar_usuario(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    username = user_to_delete.username
    
    db.session.delete(user_to_delete)
    db.session.commit()
    flash(f'Usuario {username} eliminado con éxito.', 'success')
    return redirect(url_for('registro_minerales.usuarios'))
    
            
#----------------------------------------------------------------------------
def load_json_from_file():

    path = os.path.join(current_app.instance_path, 'apiResponse.json')
    path = os.path.normpath(path)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_json_to_file(data):
    path = os.path.join(current_app.instance_path, 'apiResponse.json')
    path = os.path.normpath(path)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        

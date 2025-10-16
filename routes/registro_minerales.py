from flask import Blueprint, render_template, request, redirect, url_for
from dotenv import load_dotenv;
import os,json;
from flask import current_app
import requests;
from models.Mineral import Mineral
from database import db

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
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']
        
        if not name or not price or not stock:
            return render_template('registro_mineral.html', error='Todos los campos son obligatorios')
        
        if Mineral.query.filter_by(name=name).first():
            return render_template('registro_mineral.html', error='El mineral ya está registrado')
        
        data = load_json_from_file()
        metals = data.get('metals', {})

        metals[name] = float(price), int(stock)
        data['metals'] = metals

        save_json_to_file(data)
        return redirect(url_for('registro_minerales.ver_stock'))
    return render_template('registro_mineral.html')





@registro_minerales_bp.route('/ver_stock')
def ver_stock():
    data = load_json_from_file()
    metals = data.get('metals', {})
    currency = data.get('currency', 'ARS')
    return render_template('ver_stock.html', metals=metals, currency=currency)


@registro_minerales_bp.route('/editar_mineral/<nombre>', methods=['GET', 'POST'])
def editar_mineral(nombre):
    data = load_json_from_file()
    metals = data.get('metals', {})

    if request.method == 'POST' :
        nuevo_nombre = request.form['name']
        nuevo_precio = request.form['price']

        if nombre in metals:
            if nuevo_nombre != nombre:
                metals.pop(nombre)
            metals[nuevo_nombre] = nuevo_precio
            data['metals'] = metals
            save_json_to_file(data)
            return redirect(url_for('registro_minerales.ver_stock'))
    
    precio_actual = metals.get(nombre)
    return render_template('editar_mineral.html', nombre=nombre, precio=precio_actual)

@registro_minerales_bp.route('/eliminar_mineral/<nombre>', methods=['POST'])
def eliminar_mineral(nombre):
    data = load_json_from_file()
    metals = data.get('metals', {})
    if nombre in metals:
        metals.pop(nombre)
        data['metals'] = metals
        save_json_to_file(data)
    return redirect(url_for('registro_minerales.ver_stock'))



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
        

from flask import Blueprint, render_template, request, redirect, url_for
from dotenv import load_dotenv;
import os,json;
from flask import current_app
import requests;

load_dotenv();

API_KEY = os.getenv('API_KEY');
URL_API = os.getenv('URL_API');


venta_minerales_bp = Blueprint('venta_minerales', __name__)

@venta_minerales_bp.route('/comprar_minerales')
def comprar_minerales():

    url = f"{URL_API}?api_key={API_KEY}&unit=kg&currency=ARS"

    headers = {}

    headers["Accept"] = "application/json"

    # resp = requests.get(url, headers=headers)
    # data = resp.json()

    data = load_json_from_file()

    currency = data['currency']
    metals = data['metals']

    return render_template('comprar_minerales.html', metals=metals, currency=currency)

def load_json_from_file():

    path = os.path.join(current_app.instance_path, 'apiResponse.json')
    path = os.path.normpath(path)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
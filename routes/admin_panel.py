from flask import Blueprint, render_template, request, Response, redirect, url_for
from dotenv import load_dotenv;
import os
import pandas as pd
from datetime import datetime
import requests
from models.User import User
from models.Mineral import Mineral

admin_panel_bp = Blueprint('admin_panel', __name__)

load_dotenv();

API_KEY = os.getenv('API_KEY');
URL_API = os.getenv('URL_API');

@admin_panel_bp.route('/admin_panel', methods=['GET'])
def admin_panel():
    section = request.args.get('page', '')

    if section not in ['usuarios', 'pedidos', 'minerales', '']:
        return redirect(url_for('admin_panel.admin_panel'))
    
    if section == 'usuarios':
        table_data = User.query.all()
    elif section == 'minerales':

        url = f"{URL_API}?api_key={API_KEY}&unit=kg&currency=ARS"

        headers = {}

        headers["Accept"] = "application/json"

        resp = requests.get(url, headers=headers)
        data = resp.json()
        
        metalsRaw = data['metals']
        table_data = metalsRaw.items()
    else:
        table_data = None

    return render_template('admin_panel.html', page=section, table_data=table_data)

@admin_panel_bp.route('/admin_panel/exportar_csv', methods=['GET'])
def exportar_csv():
    section = request.args.get('page', '')

    if section not in ['usuarios', 'pedidos', 'minerales']:
        return redirect(url_for('admin_panel.admin_panel'))
    
    if section == 'usuarios':
        users = User.query.all()
        data = [{'ID': user.id, 'Email': user.mail, 'Role': user.role} for user in users]
        df = pd.DataFrame(data)
    elif section == 'minerales':
        url = f"{URL_API}?api_key={API_KEY}&unit=kg&currency=ARS"

        headers = {}

        headers["Accept"] = "application/json"

        resp = requests.get(url, headers=headers)
        data = resp.json()
        
        metalsRaw = data['metals']
        data = [{'Mineral': metal, 'Precio': precio} for metal, precio in metalsRaw.items()]
        df = pd.DataFrame(data)

    csv_data = df.to_csv(index=False)
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment;filename={section}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'}
    )


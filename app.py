import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager, login_user,
    logout_user, login_required, current_user
)
from authlib.integrations.flask_client import OAuth

from dotenv import load_dotenv;

load_dotenv()

from database import db, init_db

from routes.venta_minerales import venta_minerales_bp
from routes.pedidos import pedidos_bp
from routes.carrito import carrito_bp
from routes.registro_minerales import registro_minerales_bp
from routes.google_auth import auth_bp

from models.User import User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minashi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_ID_CLIENT')

app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_SECRET_CLIENT')

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs'
)

app.google = google

init_db(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(venta_minerales_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(carrito_bp)
app.register_blueprint(registro_minerales_bp)
app.register_blueprint(auth_bp)


@app.route('/')
def home():
    if current_user.is_authenticated:
        user = True;
    else:
        user = False;
    return render_template('home.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mail = request.form['mail']
        confirm_password = request.form['confirm_password']

        passFormatted = Bcrypt().generate_password_hash(password).decode('utf-8')

        if password != confirm_password:
            return render_template('register.html', error='Las contraseñas no coinciden')
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='El nombre de usuario ya existe')
        
        if User.query.filter_by(mail=mail).first():
            return render_template('register.html', error='El correo ya está registrado')
        
        new_user = User(username=username, password=passFormatted, mail=mail, role='user')
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        userDB = User.query.filter_by(username=username).first()

        if userDB and Bcrypt().check_password_hash(userDB.password, password):
            userDB.cart = session.get('cart', [])
            login_user(userDB)
            return redirect(url_for('home'))
        
        else:
            return render_template('login.html', error='Credenciales invalidas')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    return render_template('perfil.html', current_user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
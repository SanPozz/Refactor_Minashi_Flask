from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager, login_user,
    logout_user, login_required, current_user
)
from database import db, init_db
from routes.venta_minerales import venta_minerales_bp
from routes.pedidos import pedidos_bp
from routes.carrito import carrito_bp
from routes.registro_minerales import registro_minerales_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minashi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Minashi-flask'

from models.User import User

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

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session
from database import db, init_db
from routes.venta_minerales import venta_minerales_bp
from routes.pedidos import pedidos_bp
from routes.carrito import carrito_bp

app = Flask(__name__)
# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minashi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Minashi-flask'

from models.User import User

init_db(app)

app.register_blueprint(venta_minerales_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(carrito_bp)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mail = request.form['mail']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('register.html', error='Las contraseñas no coinciden')
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='El nombre de usuario ya existe')
        
        if User.query.filter_by(mail=mail).first():
            return render_template('register.html', error='El correo ya está registrado')
        
        new_user = User(username=username, password=password, mail=mail, role='user')
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if 'user' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        userDB = User.query.filter_by(username=username).first()
        if userDB and userDB.password == password:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Credenciales invalidas')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
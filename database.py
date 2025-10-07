from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def init_db(appParam):

    db.init_app(appParam)
    
    with appParam.app_context():
        try:
            db.create_all()
            print("Base de datos inicializada correctamente")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
            raise e
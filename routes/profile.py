
import os
import boto3
from flask import Blueprint, request,render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from database import db  
from models.User import User 
from flask_login import login_user, current_user

profile_bp = Blueprint('profile_bp', __name__)

S3_BUCKET = os.getenv('S3_BUCKET')
S3_KEY = os.getenv('AWS_ACCESS_KEY')
S3_SECRET = os.getenv('AWS_SECRET_KEY')
S3_REGION = os.getenv('S3_REGION')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_bp.route('/mi_perfil', methods=['GET'])
@login_required
def perfil():
    return render_template('perfil.html')

@profile_bp.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
   

    if 'profile_picture' not in request.files:
        flash('No se seleccionó ningún archivo.', 'danger')
        return redirect(url_for('profile_bp.perfil'))
    
    file = request.files['profile_picture']
    
  
    if file.filename == '' or not allowed_file(file.filename):
        flash('Formato de archivo inválido. Solo se permiten imágenes.', 'danger')
        return redirect(url_for('profile_bp.perfil'))

    if file:
    
        filename = secure_filename(file.filename)
      
        s3_filename = f"perfiles/user_{current_user.id}_{filename}"
        
        s3 = boto3.client(
            's3',
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET,
            region_name=S3_REGION
        )

        try:
        
            s3.upload_fileobj(
                file,
                S3_BUCKET,
                s3_filename
           
            )
            
            
            s3_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{s3_filename}"
            
            
            current_user.url = s3_url
            print(current_user.url)
            db.session.commit()
            login_user(current_user)
            flash('Foto de perfil actualizada exitosamente!', 'success')
            return redirect(url_for('profile_bp.perfil'))

        except Exception as e:
            flash(f"Error al subir la imagen a S3: {e}", 'danger')
            return redirect(url_for('profile_bp.perfil'))
    
    return redirect(url_for('profile_bp.perfil'))


from flask import Blueprint, current_app, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_login import login_user
from dotenv import load_dotenv
import os

load_dotenv()

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login/google")
def login():
    google = current_app.google
    redirect_uri = url_for("auth.authorize", _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route("/authorize")
def authorize():
    google = current_app.google;
    token = google.authorize_access_token();
    
    user_info = token.get("userinfo")
    if user_info is None:
        user_info = google.get("userinfo").json();

    google_id = user_info["sub"];
    email = user_info["email"];
    username = user_info["name"]
    role = 'user';
    password = 'google_oauth';

    from models.User import User

    user = User.query.filter_by(mail=email).first()

    if not user:
        user = User(username=username, mail=email, role=role, password=password)
        from database import db
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect(url_for("profile"))
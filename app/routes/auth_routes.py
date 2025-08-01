from flask import Blueprint, redirect, url_for, flash
from app.controllers.auth_controller import AuthController
from flask_login import logout_user
from flask_login import login_required


auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


@auth_bp.route('/test')
def test():
    print(" Route de test appelée")
    return "OK"

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("Route /auth/login appelée")
    return AuthController.login()

@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    return AuthController.logout()


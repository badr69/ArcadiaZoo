from flask import Blueprint, render_template

from app.forms.auth_forms import LoginForm

auth_bp = Blueprint('auth_bp', __name__, url_prefix="/auth")


@auth_bp.route('/auth/login')
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)
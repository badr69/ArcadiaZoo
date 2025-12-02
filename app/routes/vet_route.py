from flask import Blueprint, render_template
from app.forms.auth_forms import LogoutForm
from flask_login import login_required, current_user

vet_bp = Blueprint('vet', __name__, url_prefix="/vet")

@vet_bp.route('/vet_dash')
@login_required
def vet_dash():
    form = LogoutForm()
    role_name = current_user.role_name if current_user else None
    return render_template('dash/vet_dash.html', form=form, role_name=role_name)


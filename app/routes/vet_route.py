from flask import Blueprint, render_template
from app.forms.auth_forms import LogoutForm
from flask_login import login_required

vet_bp = Blueprint('vet', __name__, url_prefix="/vet")

@vet_bp.route('/vet_dash')
@login_required
def vet_dash():
    form = LogoutForm()
    return render_template('dash/vet_dash.html', form=form)


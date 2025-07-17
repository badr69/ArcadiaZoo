from flask import Blueprint, render_template
from app.forms.auth_forms import LogoutForm


vet_bp = Blueprint('vet', __name__, url_prefix="/vet")

@vet_bp.route('/vet_dash')
def vet_dash():
    form = LogoutForm()
    return render_template('dash/vet_dash.html', form=form)


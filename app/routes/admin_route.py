from flask import Blueprint, render_template
from app.forms.auth_forms import LogoutForm
from flask_login import login_required

admin_bp = Blueprint('admin', __name__, url_prefix="/admin")

@admin_bp.route('/admin_dash')
@login_required
def admin_dash():
    form = LogoutForm()
    return render_template('dash/admin_dash.html', form=form)


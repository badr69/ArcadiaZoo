from flask import Blueprint, render_template
from app.forms.auth_forms import LogoutForm
from flask_login import login_required

employee_bp = Blueprint('employee', __name__, url_prefix="/employee")


@employee_bp.route('/employee_dash')
@login_required
def employee_dash():
    form = LogoutForm()
    return render_template('dash/employee_dash.html', form=form)


from flask import Blueprint, render_template
from app.forms.auth_forms import LogoutForm


employee_bp = Blueprint('employee', __name__, url_prefix="/employee")

@employee_bp.route('/employee_dash')
def employee_dash():
    form = LogoutForm()
    return render_template('dash/employee_dash.html', form=form)


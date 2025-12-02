from flask import Blueprint, render_template
from app.forms.auth_forms import LogoutForm
from flask_login import login_required, current_user
from app.utils.decorators import roles_required


employee_bp = Blueprint('employee', __name__, url_prefix="/employee")

@employee_bp.route('/employee_dash')
@login_required
@roles_required("admin", "employee")
def employee_dash():
    form = LogoutForm()
    role_name = current_user.role_name if current_user else None
    return render_template('dash/employee_dash.html', form=form, role_name=role_name)

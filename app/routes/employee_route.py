from flask import Blueprint, render_template
from app.forms.auth_forms import LogoutForm
from flask_login import login_required, current_user
from app.utils.decorators import roles_required


employee_bp = Blueprint('employee', __name__, url_prefix="/employee")

@employee_bp.route('/employee_dash')
@login_required
@roles_required("employee", "admin")
def employee_dash():
    form = LogoutForm()
    role = current_user.role if current_user else None
    return render_template('dash/employee_dash.html', form=form, role=role)

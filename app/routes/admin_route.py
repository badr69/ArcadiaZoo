from flask import Blueprint, render_template
from app.forms.auth_forms import LogoutForm
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, url_prefix="/admin")


@admin_bp.route("/admin/admin_dash")
@login_required
def admin_dash():
    form = LogoutForm()
    # Utiliser role_name à la place de role
    role_name = current_user.role_name if current_user else None

    # Tu peux passer role_name au template
    return render_template("dash/admin_dash.html", form=form, role_name=role_name)


# @admin_bp.route('/admin_dash')
# @login_required
# def admin_dash():
#     form = LogoutForm()
#     role = current_user.role if current_user else None
#     return render_template('dash/admin_dash.html', form=form, role=role)
#

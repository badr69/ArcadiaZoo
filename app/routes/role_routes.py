from flask import Blueprint
from app.controllers.role_controller import RoleController
from app.utils.decorators import roles_required
from flask_login import login_required, current_user

role_bp = Blueprint("role", __name__, url_prefix="/role")

# ✅ Une seule instance partagée dans toutes les routes
role_controller = RoleController()


@role_bp.route("/list_all_roles", methods=["GET"])
@login_required
@roles_required("admin")
def list_all_roles():
    print(
        f"DEBUG — current_user: {current_user.username}, role_id={current_user.role_id}, role_name={getattr(current_user, 'role_name', None)}"
    )
    return role_controller.list_all_roles()


@role_bp.route("/<int:role_id>", methods=["GET"])
@login_required
@roles_required("admin")
def get_role_by_id(role_id):
    return role_controller.get_role_by_id(role_id)


@role_bp.route("/create_role", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def create_role():
    return role_controller.create_role()


@role_bp.route("/update_role/<int:role_id>", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def update_role(role_id):
    return role_controller.update_role(role_id)


@role_bp.route("/delete_role/<int:role_id>", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def delete_role(role_id):
    return role_controller.delete_role(role_id)

from flask import Blueprint
from app.controllers.role_controller import RoleController
from app.utils.decorators import roles_required
from flask_login import login_required


role_bp = Blueprint("role", __name__, url_prefix="/role")

@role_bp.route("/list_all_roles", methods=["GET"])
@login_required
@roles_required("admin")
def list_all_roles():
    return RoleController.list_all_roles()

@role_bp.route("/<int:role_id>", methods=["GET"])
@login_required
@roles_required("admin")
def get_role_by_id(role_id):
    return RoleController.get_role_by_id(role_id)

@role_bp.route("/create_role", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def create_role():
    return RoleController.create_role()

@role_bp.route("/update_role/<int:role_id>", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def update_role(role_id):
    return RoleController.update_role(role_id)

@role_bp.route("/delete_role/<int:role_id>", methods=["POST"])
@login_required
@roles_required("admin")
def delete_role(role_id):
    return RoleController.delete_role(role_id)




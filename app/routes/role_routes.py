from flask import Blueprint
from app.controllers.role_controller import RoleController
from app.utils.decorators import admin_required

role_bp = Blueprint("role_bp", __name__, url_prefix="/role")

@role_bp.route("/list_all_roles", methods=["GET"])

def list_all_roles():
    return RoleController.list_all_roles()

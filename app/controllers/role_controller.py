from app.services.role_service import RoleService
from flask import render_template


class RoleController:
    @staticmethod
    def list_all_roles():
        roles = RoleService.get_all_roles()
        return render_template("role/list_all_roles.html", roles=roles)


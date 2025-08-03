from app.services.role_service import RoleService
from flask import render_template

class RoleController:
    @staticmethod
    def list_all_roles():
        # TODO: Récupérer tous les rôles via le service métier
        roles = RoleService.get_all_roles()
        # TODO: Afficher la liste des rôles dans le template approprié
        return render_template("role/list_all_roles.html", roles=roles)


# from app.services.role_service import RoleService
# from flask import render_template
#
#
# class RoleController:
#     @staticmethod
#     def list_all_roles():
#         roles = RoleService.get_all_roles()
#         return render_template("role/list_all_roles.html", roles=roles)
#

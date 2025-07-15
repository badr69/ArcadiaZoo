# app/services/role_service.py
from app.models.role_model import RoleModel

class RoleService:
    @staticmethod
    def list_all_roles():
        return RoleModel.list_all_roles()





# from app.models.role_model import RoleModel
# from app.models.role_model import Role
#
# class RoleService:
#
#     @staticmethod
#     def list_all_roles():
#         roles = RoleModel.list_all_roles()
#         role_objects = [Role(r[0], r[1]) for r in roles]
#         return role_objects
#



from app.models.role_model import RoleModel

class RoleService:
    @staticmethod
    def list_all_roles():
        return RoleModel.list_all_roles()




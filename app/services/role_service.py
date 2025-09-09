from app.models.role_model import RoleModel

class RoleService:
    @staticmethod
    def list_all_roles():
        return (RoleModel.list_all_roles())

    @staticmethod
    def get_role_by_id(role_id):
        return RoleModel.get_role_by_id(role_id)

    @staticmethod
    def create_role(name):
        return RoleModel.create_role(name)

    @staticmethod
    def update_role(role_id, name):
        return RoleModel.update_role(role_id, name)

    @staticmethod
    def delete_role(role_id):
        return RoleModel.delete_role(role_id)

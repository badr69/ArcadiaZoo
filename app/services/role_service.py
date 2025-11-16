from app.models.role_model import RoleModel

class RoleService:
    """Service métier pour gérer un rôle."""

    def __init__(self, role: RoleModel):
        self.role = role


    @staticmethod
    def list_all_roles():
        return RoleModel.list_all_roles()  # retourne bien une liste de RoleModel

    @staticmethod
    def get_role_by_id(role_id: int):
        return RoleModel.get_role_by_id(role_id)

    @classmethod
    def create_role(cls, name: str):
        """Crée un nouveau rôle et retourne un objet RoleService."""
        name = name.strip()
        if len(name) < 2:
            print("[create_role error]: le nom doit contenir au moins 2 caractères")
            return None

        # Vérifier unicité
        existing_roles = RoleModel.list_all_roles()
        if any(r.name.lower() == name.lower() for r in existing_roles):
            print(f"[create_role error]: le rôle '{name}' existe déjà")
            return None

        role = RoleModel.create_role(name)
        if role:
            return cls(role)
        return None

    def update_role(self, name: str):
        """Met à jour le nom du rôle et retourne self."""
        name = name.strip()
        if len(name) < 2:
            print("[update_role error]: le nom doit contenir au moins 2 caractères")
            return None

        # Vérifier unicité
        existing_roles = RoleModel.list_all_roles()
        if any(r.name.lower() == name.lower() and r.role_id != self.role.role_id for r in existing_roles):
            print(f"[update_role error]: le rôle '{name}' existe déjà")
            return None

        updated_role = self.role.update_role(name)
        if updated_role:
            self.role = updated_role
            return self
        return None

    def delete_role(self):
        """Supprime le rôle si autorisé et retourne True/False."""
        if self.role.name.lower() == "admin":
            print("[delete_role error]: impossible de supprimer le rôle admin")
            return False
        return self.role.delete_role()

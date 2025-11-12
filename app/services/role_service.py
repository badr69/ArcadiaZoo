from app.models.role_model import RoleModel

class RoleService:
    """Service métier pour la gestion des rôles."""

    def list_all_roles(self):
        """Retourne la liste de tous les rôles."""
        return RoleModel.list_all_roles()

    def get_role_by_id(self, role_id):
        """Retourne un rôle par son ID."""
        return RoleModel.get_role_by_id(role_id)

    def create_role(self, name):
        """Crée un rôle avec logique métier.

        - Vérifie si le nom existe déjà.
        """
        roles = RoleModel.list_all_roles()
        if any(r.name.lower() == name.lower() for r in roles):
            return None, "Ce rôle existe déjà."

        role = RoleModel.create_role(name)
        if not role:
            return None, "Erreur lors de la création du rôle."

        return role, "Rôle créé avec succès."

    def update_role(self, role, name):
        """Met à jour un rôle existant."""
        # Vérifier si le nom est déjà utilisé
        roles = RoleModel.list_all_roles()
        if any(r.name.lower() == name.lower() and r.role_id != role.role_id for r in roles):
            return {"error": "Ce nom de rôle existe déjà."}, 400

        return role.update_role(name=name)

    def delete_role(self, role):
        """Supprime un rôle."""
        return role.delete_role()

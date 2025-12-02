from app.models.role_model import RoleModel
from app.utils.security import sanitize_html, detect_sql_injection

class RoleService:
    """
    Service pour gérer la logique métier des rôles.
    """

    @property
    def id(self):
        return self.role.role_id

    @property
    def name(self):
        return self.role.name

    @property
    def created_at(self):
        return self.role.created_at

    # =========================================================================
    # MÉTHODES DE CLASSE (LIST, GET, CREATE)
    # =========================================================================

    @classmethod
    def list_all_roles(cls):
        """Retourne tous les rôles sous forme d'instances RoleService"""
        roles = RoleModel.list_all_roles()
        return [cls(role) for role in roles]

    @classmethod
    def get_role_by_id(cls, role_id):
        """Retourne un RoleService ou None si introuvable"""
        role = RoleModel.get_role_by_id(role_id)
        if not role:
            return None, "Rôle introuvable."
        return cls(role), None

    @classmethod
    def create_role(cls, name):
        """
        Crée un rôle après validation.
        Retourne RoleService si succès, None et message sinon.
        """
        name = sanitize_html(name.strip())
        if detect_sql_injection(name):
            return None, "Entrée invalide détectée."
        if len(name) < 2:
            return None, "Le nom doit contenir au moins 2 caractères."

        # Vérifier unicité
        existing_roles = RoleModel.list_all_roles()
        if any(r.name.lower() == name.lower() for r in existing_roles):
            return None, f"Le rôle '{name}' existe déjà."

        role = RoleModel.create_role(name)
        if not role:
            return None, "Erreur lors de la création du rôle."

        return cls(role), None

    # =========================================================================
    # MÉTHODES D’INSTANCE (UPDATE, DELETE)
    # =========================================================================

    def __init__(self, role: RoleModel):
        self.role = role

    def exists(self):
        """Vérifie si le rôle existe"""
        return self.role is not None

    def update_role(self, name):
        """
        Met à jour un rôle après validation.
        Retourne True si succès, False et message sinon.
        """
        if not self.exists():
            return False, "Rôle introuvable."

        name = sanitize_html(name.strip())
        if detect_sql_injection(name):
            return False, "Entrée invalide détectée."

        if len(name) < 2:
            return False, "Le nom doit contenir au moins 2 caractères."

        # Vérifier unicité pour les autres rôles
        existing_roles = RoleModel.list_all_roles()
        if any(r.name.lower() == name.lower() and r.role_id != self.role.role_id for r in existing_roles):
            return False, f"Le rôle '{name}' existe déjà."

        updated_role = self.role.update_role(name)
        if not updated_role:
            return False, "Erreur lors de la mise à jour."

        self.role = updated_role
        return True, None

    def delete_role(self):
        """
        Supprime un rôle après vérification.
        Impossible de supprimer le rôle admin.
        """
        if not self.exists():
            return False, "Rôle introuvable."

        if self.role.name.lower() == "admin":
            return False, "Impossible de supprimer le rôle admin."

        success = self.role.delete_role()
        if not success:
            return False, "Erreur lors de la suppression."
        return True, None

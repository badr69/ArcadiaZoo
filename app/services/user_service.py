from app.models.user_model import UserModel
from app.utils.security import sanitize_html, detect_sql_injection, verify_password
from app.utils.validator import is_valid_email, is_strong_password
from werkzeug.security import generate_password_hash


class UserService:
    """
    Service pour gérer la logique métier des utilisateurs.
    """

    # =====================================
    # ==== MÉTHODES DE CLASSE (CRUD) ======
    # =====================================

    @classmethod
    def authenticate(cls, email, password):
        """Authentifie un utilisateur."""
        if not email or not password:
            return None, "Email et mot de passe requis."

        user = UserModel.get_user_by_email(email)
        if not user:
            return None, "Utilisateur introuvable."

        if not verify_password(user.password_hash, password):
            return None, "Mot de passe incorrect."

        return user, None

    @classmethod
    def list_all_users(cls):
        return UserModel.list_all_users()

    @classmethod
    def list_all_vets(cls):
        return UserModel.list_all_vets()

    @classmethod
    def list_all_employees(cls):
        return UserModel.list_all_employees()

    @classmethod
    def get_user_by_id(cls, user_id):
        user = UserModel.get_user_by_id(user_id)
        if not user:
            return None, "Utilisateur introuvable."
        return user, None

    @classmethod
    def get_user_by_email(cls, email):
        email = sanitize_html(email).lower()
        user = UserModel.get_user_by_email(email)
        if not user:
            return None, "Utilisateur introuvable."
        return user, None

    @classmethod
    def create_user(cls, username, email, password, role_id):
        """Crée un nouvel utilisateur avec validation et sanitation."""
        username = sanitize_html(username)
        email = sanitize_html(email).lower()

        # Détection injection SQL
        if detect_sql_injection(username) or detect_sql_injection(email):
            return None, "Entrée invalide détectée."

        # Validations
        if not username or len(username) < 3:
            return None, "Le nom d'utilisateur doit contenir au moins 3 caractères."
        if not is_valid_email(email):
            return None, "Email invalide."
        if not is_strong_password(password):
            return None, "Mot de passe trop faible."

        # Vérifier unicité email
        if UserModel.get_user_by_email(email):
            return None, "Cet email est déjà utilisé."

        # Hachage du mot de passe
        password_hash = generate_password_hash(password)

        # Création de l'utilisateur
        user = UserModel.create_user(username, email, password_hash, role_id)
        if not user:
            return None, "Erreur lors de la création de l'utilisateur."

        return user, None

    # =====================================
    # ==== MÉTHODES D’INSTANCE ============
    # =====================================

    def __init__(self, user_id):
        self.user = UserModel.get_user_by_id(user_id)

    def exists(self):
        return self.user is not None

    def update_user(self, username, email, role_id, password=None):
        if not self.exists():
            return False, "Utilisateur introuvable."

        username = sanitize_html(username)
        email = sanitize_html(email).lower()

        if detect_sql_injection(username) or detect_sql_injection(email):
            return False, "Entrée invalide détectée."

        if not username or len(username) < 3:
            return False, "Le nom d'utilisateur doit contenir au moins 3 caractères."
        if not is_valid_email(email):
            return False, "Email invalide."

        # Vérifier si email déjà utilisé par un autre utilisateur
        existing_user = UserModel.get_user_by_email(email)
        if existing_user and existing_user.user_id != self.user.user_id:
            return False, "Cet email est déjà utilisé."

        # Hachage du mot de passe si fourni
        password_hash = generate_password_hash(password) if password else None

        success = self.user.update_user(
            username=username,
            email=email,
            role_id=role_id,
            password_hash=password_hash
        )
        if not success:
            return False, "Erreur lors de la mise à jour."

        return True, None

    def delete_user(self):
        if not self.exists():
            return False, "Utilisateur introuvable."

        success = self.user.delete_user()
        if not success:
            return False, "Erreur lors de la suppression."

        return True, None

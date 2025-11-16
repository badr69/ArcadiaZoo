from app.models.user_model import UserModel
from app.utils.security import hash_password
from app.db.psql import get_db_connection


class UserService:
    """Service OOP pour gérer la logique métier des utilisateurs."""

    def __init__(self, user: UserModel):
        """Initialise le service pour un utilisateur spécifique."""
        self.user = user

    # ===================== CREATE / CLASSMETHOD =====================
    @classmethod
    def list_all_users(cls):
        """Retourne tous les utilisateurs sous forme d'objets UserModel."""
        return UserModel.list_all_users()

    @classmethod
    def get_user_by_id(cls, user_id):
        """Retourne un objet UserModel par son ID, ou None si inexistant."""
        user = UserModel.get_user_by_id(user_id)
        return cls(user) if user else None

    @classmethod
    def get_user_by_email(cls, email):
        """Retourne un objet UserService pour un utilisateur via email."""
        user = UserModel.get_user_by_email(email)
        return cls(user) if user else None

    @classmethod
    def create_user(cls, username, email, password, role_id):
        """
        Crée un nouvel utilisateur et retourne un objet UserService.
        Retourne None si échec (ex: email déjà utilisé).
        """
        if UserModel.get_user_by_email(email):
            return None  # Email déjà utilisé
        user = UserModel.create_user(username, email, password, role_id)
        return cls(user) if user else None

    # ===================== INSTANCE METHODS =====================
    def update_user(self, username=None, email=None, role_id=None, password=None):
        """
        Met à jour l'utilisateur actuel.
        Retourne self si succès, None sinon.
        """
        # Vérification email unique
        if email and email != self.user.email:
            existing = UserModel.get_user_by_email(email)
            if existing:
                print("[update_user error]: email déjà utilisé")
                return None

        # Mise à jour des champs via le modèle
        res, status = self.user.update_user(username, email, role_id)
        if not res:
            return None

        # Mise à jour du mot de passe si fourni
        if password:
            password_hash = hash_password(password)
            try:
                with get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "UPDATE users SET password_hash = %s WHERE user_id = %s",
                            (password_hash, self.user.user_id)
                        )
                        conn.commit()
                        self.user.password_hash = password_hash
            except Exception as e:
                print(f"[update password error]: {e}")
                return None

        return self

    def delete_user(self):
        """Supprime l'utilisateur actuel. Retourne True si succès, False sinon."""
        return self.user.delete_user()

    # ===================== AUTHENTICATION =====================
    @classmethod
    def authenticate(cls, email, password):
        """
        Authentifie un utilisateur.
        Retourne un objet UserService si succès, None sinon.
        """
        user = UserModel.authenticate(email, password)
        return cls(user) if user else None

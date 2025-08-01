import psycopg2
from app.models.user_model import UserModel
from werkzeug.security import generate_password_hash


class UserService:

    @staticmethod
    def create_user(username: str, email: str, password: str, role_id: int):

        try:
            if UserModel.get_by_email(email):
                return {"error": "Email déjà utilisé."}, 400

            # Hasher le mot de passe avant la création
            hashed_password = generate_password_hash(password, method="scrypt")

            # Utiliser le mot de passe hashé pour créer l'utilisateur
            user = UserModel.create_user(username, email, hashed_password, role_id)
            if not user:
                raise Exception("Création utilisateur échouée.")

            return {
                "message": "Utilisateur créé avec succès.",
                "user_id": user.id
            }, 201

        except psycopg2.Error as db_err:
            print("[PostgreSQL] create_user:", db_err)
            return {"error": "Erreur lors de la création de l'utilisateur."}, 500
        except Exception as exc:
            print("[Service] create_user:", exc)
            return {"error": "Erreur serveur."}, 500

    @staticmethod
    def list_all_users():
        """Retourne la liste des utilisateurs (ou [] en cas d'erreur)."""
        try:
            return UserModel.list_all_users()
        except Exception as exc:
            print("[Service] list_all_users:", exc)
            return []

    @staticmethod
    def get_user_by_id(user_id: int):
        """Retourne un objet User ou None."""
        try:
            return UserModel.get_user_by_id(user_id)
        except Exception as exc:
            print("[Service] get_user_by_id:", exc)
            return None

    #
    @staticmethod
    def update_user(user_id, username, email, role_id):
        """Retourne un objet User ou None."""
        try:
            return UserModel.update_user(user_id, username, email, role_id)
        except Exception as exc:
            print("[Service] get_user_by_id:", exc)
            return None

    @staticmethod
    def delete_user(user_id: int):

        try:
            success = UserModel.delete_user(user_id)
            if not success:
                return {"error": "Utilisateur non trouvé."}, 404
            return {"message": "Utilisateur supprimé."}, 200
        except Exception as exc:
            print("[Service] delete_user:", exc)
            return {"error": "Erreur serveur."}, 500

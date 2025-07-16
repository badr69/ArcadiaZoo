import psycopg2
from app.db.psql import get_db_connection
from app.models.user_model import UserModel
from werkzeug.security import generate_password_hash



class UserService:

        def create_user(username, email, password, role_id):
            hashed_password = generate_password_hash(password)
            return UserModel.create_user(username, email, hashed_password, role_id)

    #
    # @staticmethod
    # def create_user(username: str, email: str, password: str, role_id: int):
    #
    #     try:
    #         if User.get_by_email(email):
    #             return {"error": "Email déjà utilisé."}, 400
    #
    #         user = User.create_user(username, email, password, role_id)
    #         if not user:
    #             raise Exception("Création utilisateur échouée.")
    #
    #         return {
    #             "message": "Utilisateur créé avec succès.",
    #             "user_id": user.id
    #         }, 201
    #
    #     except psycopg2.Error as db_err:
    #         print("[PostgreSQL] create_user:", db_err)
    #         return {"error": "Erreur lors de la création de l'utilisateur."}, 500
    #     except Exception as exc:
    #         print("[Service] create_user:", exc)
    #         return {"error": "Erreur serveur."}, 500


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
        # @staticmethod
        # def update_user(user_id: int, username: str, email: str, role_id: int):
        #
        #     conn = cur = None
        #     try:
        #         # ---------- validation de l'existence du rôle ----------
        #         conn = get_db_connection()
        #         cur = conn.cursor()
        #         cur.execute("SELECT id FROM roles WHERE id = %s", (role_id,))
        #         if cur.fetchone() is None:
        #             return {"error": "Rôle inexistant."}, 400
        #
        #         # ---------- mise à jour ----------
        #         with conn.cursor() as cur2:
        #             cur2.execute("""
        #                 UPDATE users
        #                 SET username = %s,
        #                     email    = %s,
        #                     role_id  = %s
        #                 WHERE id = %s
        #                 RETURNING id
        #             """, (username, email, role_id, user_id))
        #             if cur2.rowcount == 0:
        #                 return {"error": "Utilisateur non trouvé."}, 404
        #
        #         conn.commit()
        #         return {"message": "Utilisateur mis à jour."}, 200
        #
        #     except psycopg2.Error as db_err:
        #         print("[PostgreSQL] update_user:", db_err)
        #         if conn:
        #             conn.rollback()
        #         return {"error": "Erreur lors de la mise à jour."}, 500
        #     except Exception as exc:
        #         print("[Service] update_user:", exc)
        #         if conn:
        #             conn.rollback()
        #         return {"error": "Erreur serveur."}, 500
        #     finally:
        #         if cur:
        #             cur.close()
        #         if conn:
        #             conn.close()

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

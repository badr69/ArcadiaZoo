import psycopg2
from app.db.psql import get_db_connection
from app.forms import UpdateUserForm
from app.models.user_model import User
from flask import url_for, flash, redirect, render_template

class UserService:

    @staticmethod
    def create_user(username, email, password, role_id):
        """
        Crée un nouvel utilisateur s'il n'existe pas déjà avec cet email.
        """
        try:
            existing_user = User.get_by_email(email)
            if existing_user:
                return {"error": "Email déjà utilisé."}, 400

            user = User.create(username, email, password, role_id)
            return {
                "message": "Utilisateur créé avec succès.",
                "user_id": user.id
            }, 201

        except psycopg2.Error as e:
            print("Erreur PostgreSQL:", e)
            return {"error": "Erreur lors de la création de l'utilisateur."}, 500
        except Exception as e:
            print("Erreur inattendue:", e)
            return {"error": "Erreur serveur."}, 500

    @staticmethod
    def get_all_users():
        """
        Récupère tous les utilisateurs.
        """
        try:
            return User.get_all_users()
        except Exception as e:
            print(f"Erreur dans get_all_users : {e}")
            return None

    @staticmethod
    def get_user_by_id(user_id):
        """
        Récupère un utilisateur par son ID.
        """
        try:
            return User.get_user_by_id(user_id)
        except Exception as e:
            print(f"Erreur dans get_user_by_id : {e}")
            return None

    from flask import render_template, request, redirect, url_for, flash
    from app.forms import UpdateUserForm  # adapte selon ton projet

    @staticmethod
    def update_user(id):
        form = UpdateUserForm()

        if form.validate_on_submit():
            # récupérer les données du form
            username = form.username.data
            email = form.email.data
            role_name = form.role_name.data

            result = UserService.update_user(id, username, email, role_name)

            if result['status']:
                flash(result['message'], 'success')
                return redirect(url_for('user_list'))
            else:
                flash(result['message'], 'danger')

        else:
            # GET : on pré-remplit le formulaire avec les données utilisateur existantes
            user = User.get_user_by_id(id)  # à adapter selon ta méthode d'accès aux données
            if not user:
                flash("Utilisateur non trouvé.", "warning")
                return redirect(url_for('user_list'))
            form.username.data = user.username
            form.email.data = user.email
            form.role_name.data = user.role_name  # ou role_name récupéré selon ta structure

        return render_template('user/update_user.html', form=form)

    # @staticmethod
    # def update_user(user_id, username, email, role_name):
    #     """
    #     Met à jour les informations d'un utilisateur, y compris son rôle.
    #     """
    #     conn = None
    #     cur = None
    #     try:
    #         conn = get_db_connection()
    #         cur = conn.cursor()
    #
    #         # Récupération de l'ID du rôle
    #         cur.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
    #         role_row = cur.fetchone()
    #         if role_row is None:
    #             print(f"Rôle '{role_name}' non trouvé.")
    #             return False
    #         role_id = role_row[0]
    #
    #         # Mise à jour de l'utilisateur
    #         success = User.update_user(user_id, username, email, role_id)
    #         return success
    #
    #     except Exception as e:
    #         print(f"Erreur dans le service update_user : {e}")
    #         return False
    #
    #     finally:
    #         if cur:
    #             cur.close()
    #         if conn:
    #             conn.close()

    @staticmethod
    def delete_user(user_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            if cur.rowcount == 0:
                print(f"Aucun utilisateur trouvé avec l'id {user_id}.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'utilisateur : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    # @staticmethod
    # def authenticate_user(email, password):
    #     try:
    #         user = User.get_by_email(email)
    #         if not user or not user.check_password(password):
    #             return {"error": "Email ou mot de passe incorrect."}, 401
    #
    #         return {
    #             "message": "Authentification réussie.",
    #             "user_id": user.id,
    #             "role": user.role_name
    #         }, 200
    #
    #     except Exception as e:
    #         print("Erreur d'authentification:", e)
    #         return {"error": "Erreur lors de l'authentification."}, 500
    #
    # @staticmethod
    # def get_user_by_email(email):
    #     try:
    #         user = User.get_by_email(email)
    #         if not user:
    #             return None
    #         return {
    #             "id": user.id,
    #             "username": user.username,
    #             "email": user.email,
    #             "role": user.role_name
    #         }
    #     except Exception as e:
    #         print("Erreur lors de la récupération de l'utilisateur:", e)
    #         return None
    #
    # @staticmethod
    # def update_user_role(email, new_role):
    #     try:
    #         user = User.get_by_email(email)
    #         if not user:
    #             return {"error": "Utilisateur introuvable."}, 404
    #
    #         conn = get_db_connection()
    #         cur = conn.cursor()
    #         try:
    #             cur.execute("""
    #                 UPDATE users SET role_name = %s WHERE email = %s
    #             """, (new_role, email))
    #             conn.commit()
    #             return {"message": "Rôle mis à jour avec succès."}, 200
    #         except psycopg2.Error as e:
    #             print("Erreur PostgreSQL:", e)
    #             return {"error": "Erreur lors de la mise à jour du rôle."}, 500
    #         finally:
    #             cur.close()
    #             conn.close()
    #
    #     except Exception as e:
    #         print("Erreur inattendue:", e)
    #         return {"error": "Erreur serveur."}, 500



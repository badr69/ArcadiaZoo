from flask import render_template, redirect, url_for, flash, request
from app.db.psql import get_db_connection
from app.forms import CreateUserForm
from app.services.user_service import UserService


class UserController:

    @staticmethod
    def create_user():
        form = CreateUserForm()
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM roles WHERE name != 'admin'")
            roles = cursor.fetchall()
            form.role_id.choices = [(role[0], role[1]) for role in roles]
        except Exception as e:
            flash(f"Erreur lors du chargement des rôles : {str(e)}", "danger")
            return render_template('user/create_user.html', form=form)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            role_id = form.role_id.data

            result, status = UserService.create_user(username, email, password, role_id)
            if status == 201:
                flash("Utilisateur créé avec succès !", "success")
                return redirect(url_for('user.get_all_users'))
            else:
                flash(result.get('error', 'Erreur lors de la création'), 'danger')

        return render_template('user/create_user.html', form=form)

    @staticmethod
    def get_all_users():
        try:
            users = UserService.get_all_users()
            if users is None:
                flash("Impossible de récupérer les utilisateurs", "warning")
                users = []
            return users
        except Exception as e:
            flash(f"Erreur : {str(e)}", "danger")
            return []

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return UserService.get_user_by_id(user_id)
        except Exception as e:
            print(f"Erreur get_user_by_id: {e}")
            return None

    @staticmethod
    def update_user(user_id):
        user = UserService.get_user_by_id(user_id)
        if user is None:
            flash("Utilisateur non trouvé", "warning")
            return redirect(url_for('user.list_all_users'))

        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            role_name = request.form.get('role')  # Assure-toi que ce nom est correct

            # Validation des champs
            if not all([username, email, role_name]):
                flash("Tous les champs sont obligatoires", "warning")
                return render_template('user/update_user.html', user=user)

            # Validation de l'email (si nécessaire)
            # try:
            #     valid_email = validate_email(email)
            #     email = valid_email.email
            # except EmailNotValidError as e:
            #     flash("Email invalide", "danger")
            #     return render_template('user/update_user.html', user=user)

            # Mise à jour de l'utilisateur
            success = UserService.update_user(user_id, username, email, role_name)
            if not success:
                flash("Erreur lors de la mise à jour de l'utilisateur", "danger")
                return render_template('user/update_user.html', user=user)

            flash("Utilisateur mis à jour avec succès", "success")
            return redirect(url_for('user.list_all_users'))  # Retour à la liste des utilisateurs

        return render_template('user/update_user.html', user=user)


    @staticmethod
    def delete_user(user_id):
        success = UserService.delete_user(user_id)
        if success:
            flash("Utilisateur supprimé avec succès", "success")
        else:
            flash("Erreur lors de la suppression de l'utilisateur", "danger")
        return redirect(url_for('user.list_all_users'))








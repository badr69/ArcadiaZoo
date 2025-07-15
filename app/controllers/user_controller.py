from flask import render_template, redirect, url_for, flash, request
from app.forms.user_forms import UpdateUserForm, CreateUserForm
from app.services.user_service import UserService
from app.services.role_service import RoleService

class UserController:

    @staticmethod
    def list_all_users():
        users = UserService.list_all_users()
        return render_template('user/list_all_users.html', users=users)

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return UserService.get_user_by_id(user_id)
        except Exception as e:
            print(f"Erreur get_user_by_id: {e}")
            return None

    @staticmethod
    def update_user(user_id):
        form = UpdateUserForm()
        user = UserService.get_user_by_id(user_id)
        if not user:
            flash("Utilisateur introuvable", "danger")
            return redirect(url_for("user.list_all_users"))

        roles = RoleService.list_all_roles()
        form.role_name.choices = [(str(r.id), r.name) for r in roles]

        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            role_id = int(form.role_name.data)

            success = UserService.update_user(user_id, username, email, role_id)
            if success:
                flash("Utilisateur mis à jour avec succès !", "success")
                return redirect(url_for("user.list_all_users"))
            else:
                flash("Erreur lors de la mise à jour", "danger")

        if request.method == "GET":
            form.username.data = user.username
            form.email.data = user.email
            form.role_name.data = str(user.role_id)

        return render_template("user/update_user.html", form=form, user=user)

    @staticmethod
    def create_user():
        form = CreateUserForm()
        roles = RoleService.list_all_roles()
        # roles = [r for r in roles if r.name.lower() != "admin"]  # exclure admin
        roles = [r for r in roles if r.id != 1] # exlure admin
        form.role_name.choices = [(str(r.id), r.name) for r in roles]

        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            role_id = int(form.role_name.data)

            success = UserService.create_user(username, email, password, role_id)
            if success:
                flash("Utilisateur créé avec succès", "success")
                return redirect(url_for("user.list_all_users"))
            else:
                flash("Erreur lors de la création", "danger")

        return render_template("user/create_user.html", form=form)

    @staticmethod
    def delete_user(user_id):
        success = UserService.delete_user(user_id)
        if success:
            flash("Utilisateur supprimé avec succès", "success")
        else:
            flash("Erreur lors de la suppression de l'utilisateur", "danger")
        return redirect(url_for('user.list_all_users'))



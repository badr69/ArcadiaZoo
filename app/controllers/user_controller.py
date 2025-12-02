from flask import render_template, redirect, url_for, flash
from app.forms.user_forms import CreateUserForm, UpdateUserForm
from app.services.user_service import UserService
from app.utils.security import sanitize_html


class UserController:

    # --------------------
    # MÉTHODES DE CLASSE / STATIC
    # --------------------
    @staticmethod
    def list_all_users():
        users = UserService.list_all_users()
        return render_template("user/list_all_users.html", users=users)

    @staticmethod
    def get_all_vets():
        return UserService.list_all_vets()

    @staticmethod
    def get_user_by_id(user_id):
        user, error = UserService.get_user_by_id(user_id)
        if error:
            flash(error, "danger")
            return redirect(url_for("user.list_all_users"))
        return render_template("user/user_details.html", user=user)

    @staticmethod
    def create_user():
        form = CreateUserForm()
        if form.validate_on_submit():
            username = sanitize_html(form.username.data)
            email = sanitize_html(form.email.data).lower()
            password = form.password.data
            role_id = form.role_id.data

            user, error = UserService.create_user(username, email, password, role_id)
            if user:
                flash("Utilisateur créé avec succès.", "success")
                return redirect(url_for("user.list_all_users"))
            flash(error, "danger")

        return render_template("user/create_user.html", form=form)

    # --------------------
    # MÉTHODES D’INSTANCE (UPDATE / DELETE)
    # --------------------
    def __init__(self, user_id):
        self.user_service = UserService(user_id)

    def update_user(self):
        if not self.user_service.exists():
            flash("Utilisateur introuvable.", "danger")
            return redirect(url_for("user.list_all_users"))

        form = UpdateUserForm(obj=self.user_service.user)

        if form.validate_on_submit():
            username = sanitize_html(form.username.data)
            email = sanitize_html(form.email.data).lower()
            role_id = form.role_id.data

            success, error = self.user_service.update_user(username, email, role_id)
            if success:
                flash("Utilisateur mis à jour avec succès.", "success")
                return redirect(url_for("user.list_all_users"))
            flash(error, "danger")

        return render_template(
            "user/update_user.html",
            form=form,
            user=self.user_service.user
        )

    def delete_user(self):
        if not self.user_service.exists():
            flash("Utilisateur introuvable.", "danger")
            return redirect(url_for("user.list_all_users"))

        success, error = self.user_service.delete_user()
        if success:
            flash("Utilisateur supprimé avec succès.", "success")
        else:
            flash(error, "danger")

        return redirect(url_for("user.list_all_users"))





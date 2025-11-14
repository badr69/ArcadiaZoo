from flask import render_template, redirect, url_for, flash, request
from app.forms.user_forms import UpdateUserForm, CreateUserForm
from app.services.user_service import UserService
from app.services.role_service import RoleService
from app.utils.security import sanitize_html, detect_sql_injection

class UserController:
    def __init__(self):
        self.user_service = UserService()
        self.role_service = RoleService()

    # ===================== CREATE =====================
    def create_user(self):
        # TODO: Instancier le formulaire de création utilisateur
        form = CreateUserForm()

        # TODO: Récupérer la liste des rôles et exclure admin (id=1)
        roles = self.role_service.list_all_roles()
        roles = [r for r in roles if r.role_id != 1]
        form.role_name.choices = [(str(r.role_id), r.name) for r in roles]

        # TODO: Valider la soumission du formulaire
        if form.validate_on_submit():
            username = sanitize_html(form.username.data)
            email = sanitize_html(form.email.data)
            password = sanitize_html(form.password.data)
            role_id = int(form.role_name.data)

            if detect_sql_injection(username) or detect_sql_injection(email):
                flash("Entrée invalide détectée.", "danger")
                return render_template("user/create_user.html", form=form)

            # TODO: Créer l’utilisateur via le service métier
            user, message = self.user_service.create_user(username, email, password, role_id)
            if user:
                flash(message, "success")
                return redirect(url_for("user.list_all_users"))
            else:
                flash(message, "danger")

        return render_template("user/create_user.html", form=form)

    # ===================== UPDATE =====================
    def update_user(self, user_id):
        form = UpdateUserForm()
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            flash("Utilisateur introuvable", "danger")
            return redirect(url_for("user.list_all_users"))

        roles = self.role_service.list_all_roles()
        roles = [r for r in roles if r.role_id != 1]
        form.role_name.choices = [(str(r.role_id), r.name) for r in roles]

        if form.validate_on_submit():
            username = sanitize_html(form.username.data)
            email = sanitize_html(form.email.data)
            role_id = int(form.role_name.data)

            if detect_sql_injection(username) or detect_sql_injection(email):
                flash("Entrée invalide détectée.", "danger")
                return render_template("user/update_user.html", form=form, user=user)

            result, status = self.user_service.update_user(user, username, email, role_id)
            if status == 200:
                flash(result.get("message"), "success")
                return redirect(url_for("user.list_all_users"))
            else:
                flash(result.get("error"), "danger")

        if request.method == "GET":
            form.username.data = user.username
            form.email.data = user.email
            form.role_name.data = str(user.role_id)

        return render_template("user/update_user.html", form=form, user=user)

    # ===================== DELETE =====================
    def delete_user(self, user_id):
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            flash("Utilisateur introuvable", "danger")
            return redirect(url_for("user.list_all_users"))

        success = self.user_service.delete_user(user)
        if success:
            flash("User deleted with success", "success")
        else:
            flash("Error when deleting User", "danger")

        return redirect(url_for('user.list_all_users'))

    # ===================== READ =====================
    @classmethod
    def list_all_users(cls):
        users = UserService().list_all_users()
        return render_template('user/list_all_users.html', users=users)

    @classmethod
    def get_user_by_id(cls, user_id):
        user = UserService().get_user_by_id(user_id)
        if not user:
            flash("Utilisateur introuvable", "danger")
            return redirect(url_for('user.list_all_users'))

        # Renvoyer un template HTML avec les infos du user
        return render_template("user/user_detail.html", user=user)





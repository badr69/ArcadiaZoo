from flask import render_template, url_for, redirect, flash, request
from app.forms.user_forms import CreateUserForm, UpdateUserForm
from app.services.user_service import UserService
from app.utils.security import sanitize_html, detect_sql_injection

class UserController:

    @staticmethod
    def list_all_users():
        """Liste tous les utilisateurs"""
        users = UserService.list_all_users()  # retourne liste de UserModel
        return render_template("user/list_all_users.html", users=users)

    @staticmethod
    def get_user_by_id(user_id):
        """Affiche un utilisateur par ID"""
        user_service = UserService.get_user_by_id(user_id)
        if not user_service:
            flash("Utilisateur non trouvé", "warning")
            return redirect(url_for("user.list_all_users"))
        return render_template("user/user_detail.html", user=user_service.user)

    @staticmethod
    def get_user_by_email():
        """Recherche un utilisateur via email (param GET)"""
        email = request.args.get("email", "").strip().lower()
        if not email:
            flash("Veuillez fournir un email.", "warning")
            return redirect(url_for("user.list_all_users"))

        email = sanitize_html(email)
        if detect_sql_injection(email):
            flash("Entrée invalide détectée.", "danger")
            return redirect(url_for("user.list_all_users"))

        user_service = UserService.get_user_by_email(email)
        if not user_service:
            flash("Aucun utilisateur trouvé avec cet email.", "warning")
            return redirect(url_for("user.list_all_users"))

        return render_template("user/user_detail.html", user=user_service.user)

    @staticmethod
    def create_user():
        """Crée un utilisateur via formulaire"""
        form = CreateUserForm()
        if form.validate_on_submit():
            username = sanitize_html(form.username.data)
            email = sanitize_html(form.email.data.lower())
            password = form.password.data
            role_id = form.role_id.data

            if detect_sql_injection(username) or detect_sql_injection(email):
                flash("Entrée invalide détectée.", "danger")
                return render_template("user/create_user.html", form=form)

            user_service = UserService.create_user(username, email, password, role_id)
            if user_service:
                flash(f"Utilisateur '{user_service.user.username}' créé avec succès", "success")
                return redirect(url_for("user.list_all_users"))
            else:
                flash("Erreur lors de la création de l'utilisateur.", "danger")

        return render_template("user/create_user.html", form=form)

    @staticmethod
    def update_user(user_id):
        """Met à jour un utilisateur"""
        user_service = UserService.get_user_by_id(user_id)
        if not user_service:
            flash("Utilisateur non trouvé", "warning")
            return redirect(url_for("user.list_all_users"))

        form = UpdateUserForm(obj=user_service.user)
        if form.validate_on_submit():
            username = sanitize_html(form.username.data)
            email = sanitize_html(form.email.data.lower())
            role_id = form.role_id.data

            if detect_sql_injection(username) or detect_sql_injection(email):
                flash("Entrée invalide détectée.", "danger")
                return render_template("user/update_user.html", form=form, user=user_service.user)

            updated_service = user_service.update_user(username=username, email=email, role_id=role_id)
            if updated_service:
                flash("Utilisateur mis à jour avec succès", "success")
                return redirect(url_for("user.list_all_users"))
            else:
                flash("Erreur lors de la mise à jour de l'utilisateur.", "danger")

        return render_template("user/update_user.html", form=form, user=user_service.user)

    @staticmethod
    def delete_user(user_id):
        """Supprime un utilisateur"""
        user_service = UserService.get_user_by_id(user_id)
        if not user_service:
            flash("Utilisateur non trouvé", "warning")
            return redirect(url_for("user.list_all_users"))

        success = user_service.delete_user()
        if success:
            flash(f"Utilisateur '{user_service.user.username}' supprimé avec succès", "success")
        else:
            flash("Erreur lors de la suppression de l'utilisateur.", "danger")

        return redirect(url_for("user.list_all_users"))

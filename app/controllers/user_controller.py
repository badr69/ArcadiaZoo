from flask import render_template, redirect, url_for, flash, request
from app.forms.user_forms import UpdateUserForm, CreateUserForm
from app.services.user_service import UserService
from app.services.role_service import RoleService
from app.utils.security import sanitize_html, detect_sql_injection
from app.utils.validator import is_valid_email, is_strong_password

class UserController:

    @staticmethod
    def list_all_users():
        # TODO: Récupérer tous les utilisateurs via le service métier
        users = UserService.list_all_users()
        # TODO: Afficher la liste des utilisateurs dans le template dédié
        return render_template('user/list_all_users.html', users=users)

    @staticmethod
    def get_user_by_id(user_id):
        # TODO: Récupérer l’utilisateur par son ID avec gestion d’erreur
        try:
            return UserService.get_user_by_id(user_id)
        except Exception as e:
            print(f"Erreur get_user_by_id: {e}")
            return None

    @staticmethod
    def create_user():
        # TODO: Instancier le formulaire de création utilisateur
        form = CreateUserForm()

        # TODO: Récupérer la liste des rôles et exclure admin (id=1)
        roles = RoleService.list_all_roles()
        roles = [r for r in roles if r.id != 1]
        form.role_name.choices = [(str(r.id), r.name) for r in roles]

        # TODO: Valider la soumission du formulaire
        if form.validate_on_submit():
            # TODO: Nettoyer les inputs pour éviter XSS
            username = sanitize_html(form.username.data)
            email = sanitize_html(form.email.data)
            password = sanitize_html(form.password.data)
            role_id = int(form.role_name.data)

            # TODO: Détecter injection SQL
            if detect_sql_injection(username) or detect_sql_injection(email):
                flash("Entrée invalide détectée.", "danger")
                return render_template("user/create_user.html", form=form)

            # TODO: Créer l’utilisateur via le service métier
            success = UserService.create_user(username, email, password, role_id)
            if success:
                flash("User created with succcess", "success")
                return redirect(url_for("user.list_all_users"))
            else:
                flash("Error when creating User", "danger")

        # TODO: Afficher le formulaire (avec erreurs éventuelles)
        return render_template("user/create_user.html", form=form)


    @staticmethod
    def update_user(user_id):
        # TODO: Instancier formulaire de mise à jour
        form = UpdateUserForm()

        # TODO: Récupérer utilisateur à modifier
        user = UserService.get_user_by_id(user_id)
        if not user:
            flash("Unfound user", "danger")
            return redirect(url_for("user.list_all_users"))

        # TODO: Récupérer les rôles (exclure admin)
        roles = RoleService.list_all_roles()
        roles = [r for r in roles if r.id != 1]
        form.role_name.choices = [(str(r.id), r.name) for r in roles]

        # TODO: Valider la soumission du formulaire
        if form.validate_on_submit():
            # TODO: Nettoyer les inputs pour éviter XSS
            username = sanitize_html(form.username.data)
            email = sanitize_html(form.email.data)
            role_id = int(form.role_name.data)

            # TODO: Détecter injection SQL
            if detect_sql_injection(username) or detect_sql_injection(email):
                flash("Entrée invalide détectée.", "danger")
                return render_template("user/create_user.html"),

            # TODO: Mettre à jour l’utilisateur via le service métier
            success = UserService.update_user(user_id, username, email, role_id)
            if success:
                flash("User updated with success!", "success")
                return redirect(url_for("user.list_all_users"))
            else:
                flash("Error when updating user", "danger")

        # TODO: Préremplir le formulaire lors d’une requête GET
        if request.method == "GET":
            form.username.data = user.username
            form.email.data = user.email
            form.role_name.data = str(user.role_id)

        # TODO: Afficher le formulaire de mise à jour
        return render_template("user/update_user.html", form=form, user=user)


    @staticmethod
    def delete_user(user_id):
        # TODO: Supprimer l’utilisateur via le service métier
        success = UserService.delete_user(user_id)
        if success:
            flash("User deleted with success", "success")
        else:
            flash("Error when deleting User", "danger")
        # TODO: Rediriger vers la liste des utilisateurs
        return redirect(url_for('user.list_all_users'))





# from flask import render_template, redirect, url_for, flash, request
# from app.forms.user_forms import UpdateUserForm, CreateUserForm
# from app.services.user_service import UserService
# from app.services.role_service import RoleService
# from app.utils.security import sanitize_html, detect_sql_injection
# from app.utils.validator import is_valid_email, is_strong_password
#
# class UserController:
#
#     @staticmethod
#     def list_all_users():
#         users = UserService.list_all_users()
#         return render_template('user/list_all_users.html', users=users)
#
#     @staticmethod
#     def get_user_by_id(user_id):
#         try:
#             return UserService.get_user_by_id(user_id)
#         except Exception as e:
#             print(f"Erreur get_user_by_id: {e}")
#             return None
#
#     @staticmethod
#     def create_user():
#         form = CreateUserForm()
#         roles = RoleService.list_all_roles()
#         roles = [r for r in roles if r.id != 1] # exlure admin
#         form.role_name.choices = [(str(r.id), r.name) for r in roles]
#
#         if form.validate_on_submit():
#             username = sanitize_html(form.username.data)
#             email = sanitize_html(form.email.data)
#             password = sanitize_html(form.password.data)
#             role_id = int(form.role_name.data)
#
#             # Vérification SQL Injection
#             if detect_sql_injection(username) or detect_sql_injection(email):
#                 flash("Entrée invalide détectée.", "danger")
#                 return render_template("user/create_user.html", form=form)
#
#             success = UserService.create_user(username, email, password, role_id)
#             if success:
#                 flash("User created with succcess", "success")
#                 return redirect(url_for("user.list_all_users"))
#             else:

#                 flash("Error when creating User", "danger")
#
#         return render_template("user/create_user.html", form=form)
#
#
#     @staticmethod
#     def update_user(user_id):
#         form = UpdateUserForm()
#         user = UserService.get_user_by_id(user_id)
#         if not user:
#             flash("Unfound user", "danger")
#             return redirect(url_for("user.list_all_users"))
#
#         roles = RoleService.list_all_roles()
#         # roles = [r for r in roles if r.name.lower() != "admin"]  # exclure admin
#         roles = [r for r in roles if r.id != 1]  # exlure admin
#         form.role_name.choices = [(str(r.id), r.name) for r in roles]
#
#         if form.validate_on_submit():
#             username = sanitize_html(form.username.data)
#             email = sanitize_html(form.email.data)
#             role_id = int(form.role_name.data)
#
#             # Vérification SQL Injection
#             if detect_sql_injection(username) or detect_sql_injection(email):
#                 flash("Entrée invalide détectée.", "danger")
#                 return render_template("user/create_user.html"),
#
#             success = UserService.update_user(user_id, username, email, role_id)
#             if success:
#                 flash("User updated with success!", "success")
#                 return redirect(url_for("user.list_all_users"))
#             else:
#                 flash("Error when updating user", "danger")
#
#         if request.method == "GET":
#             form.username.data = user.username
#             form.email.data = user.email
#             form.role_name.data = str(user.role_id)
#
#         return render_template("user/update_user.html", form=form, user=user)
#
#
#     @staticmethod
#     def delete_user(user_id):
#         success = UserService.delete_user(user_id)
#         if success:
#             flash("User deleted with success", "success")
#         else:
#             flash("Error when deleting User", "danger")
#         return redirect(url_for('user.list_all_users'))
#
#

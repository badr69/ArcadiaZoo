from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models.user_model import UserModel
from app.forms.auth_forms import LoginForm
from app.utils.security import verify_password


class AuthController:

    @classmethod
    def _get_redirect_by_role(cls, user):
        # TODO: Définir les redirections selon le rôle de l'utilisateur
        role_redirects = {
            "admin": "admin.admin_dash",
            "employee": "employee.employee_dash",
            "vet": "vet.vet_dash"
        }
        return role_redirects.get(user.role_name)

    @classmethod
    def login(cls):
        # TODO: Instancier le formulaire de connexion
        form = LoginForm()

        # TODO: Détecter si la requête vient d'un fetch/ajax pour renvoyer JSON ou HTML
        is_fetch = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        if request.method == 'POST':
            # TODO: Valider les données du formulaire
            if form.validate_on_submit():
                # TODO: Chercher l'utilisateur par email
                user = UserModel.get_user_by_email(form.email.data)

                # TODO: Vérifier que l'utilisateur existe et que le mot de passe est correct
                if user and verify_password(user.password_hash, form.password.data):
                    # TODO: Connecter l'utilisateur avec Flask-Login
                    login_user(user)

                    # TODO: Si requête AJAX (fetch), renvoyer un JSON avec la redirection selon rôle
                    redirect_endpoint = cls._get_redirect_by_role(user)
                    if not redirect_endpoint:
                        # TODO: Gérer rôle inconnu avec erreur
                        if is_fetch:
                            return jsonify({"success": False, "message": "Rôle inconnu"}), 400
                        flash("Rôle inconnu", "danger")
                        return redirect(url_for('auth.login'))

                    if is_fetch:
                        return jsonify({"success": True, "redirect": url_for(redirect_endpoint)})

                    # TODO: Sinon requête classique, afficher flash message succès puis rediriger selon rôle
                    flash(f"Bienvenue {user.username} !", "success")
                    return redirect(url_for(redirect_endpoint))
                else:
                    # TODO: Identifiants incorrects → message erreur JSON ou flash selon requête
                    if is_fetch:
                        return jsonify({"success": False, "message": "Email ou mot de passe incorrect"}), 401
                    flash("Email ou mot de passe incorrect", "danger")
                    return redirect(url_for('auth.login'))
            else:
                # TODO: Formulaire invalide → renvoyer erreurs au format JSON ou flash message
                if is_fetch:
                    return jsonify({"success": False, "errors": form.errors}), 400
                flash("Formulaire invalide", "danger")
                return redirect(url_for('auth.login'))

        # TODO: Pour une requête GET, afficher le formulaire de connexion
        return render_template('auth/login.html', form=form)

    @classmethod
    def logout(cls):
        # TODO: Accepter uniquement POST pour déconnexion pour éviter les attaques CSRF
        if request.method == 'POST':
            logout_user()
            flash("You are disconnected", "success")
            return redirect(url_for('auth.login'))

        # TODO: Pour toute autre méthode HTTP, refuser la requête avec message et rediriger
        flash("Méthode non autorisée", "danger")
        return redirect(url_for('auth.login'))




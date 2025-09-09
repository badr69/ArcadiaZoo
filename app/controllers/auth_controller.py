from flask import render_template, request, jsonify
from app.models.user_model import UserModel
from app.forms.auth_forms import LoginForm
from flask_login import login_user, logout_user
from flask import redirect, url_for, flash
from app.utils.security import verify_password


class AuthController:

    @staticmethod
    def login():
        # TODO: Instancier le formulaire de connexion
        form = LoginForm()

        # TODO: Détecter si la requête vient d'un fetch/ajax pour renvoyer JSON ou HTML
        is_fetch = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        if request.method == 'POST':
            # TODO: Valider les données du formulaire
            if form.validate_on_submit():
                # TODO: Chercher l'utilisateur par email
                user = UserModel.get_by_email(form.email.data)

                # TODO: Vérifier que l'utilisateur existe et que le mot de passe est correct
                if user and verify_password(user.password_hash, form.password.data):
                    # TODO: Connecter l'utilisateur avec Flask-Login
                    login_user(user)

                    # TODO: Si requête AJAX (fetch), renvoyer un JSON avec la redirection selon rôle
                    if is_fetch:
                        if user.role_name == 'admin':
                            return jsonify({"success": True, "redirect": url_for('admin.admin_dash')})
                        elif user.role_name == 'employee':
                            return jsonify({"success": True, "redirect": url_for('employee.employee_dash')})
                        elif user.role_name == 'vet':
                            return jsonify({"success": True, "redirect": url_for('vet.vet_dash')})
                        else:
                            # TODO: Gérer rôle inconnu avec erreur
                            return jsonify({"success": False, "message": "Rôle inconnu"}), 400

                    # TODO: Sinon requête classique, afficher flash message succès puis rediriger selon rôle
                    flash(f"Bienvenue {user.username} !", "success")
                    if user.role_name == 'admin':
                        return redirect(url_for('admin.admin_dash'))
                    elif user.role_name == 'employee':
                        return redirect(url_for('employee.employee_dash'))
                    elif user.role_name == 'vet':
                        return redirect(url_for('vet.vet_dash'))

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

    @staticmethod
    def logout():
        # TODO: Accepter uniquement POST pour déconnexion pour éviter les attaques CSRF
        if request.method == 'POST':
            logout_user()
            flash("Vous êtes déconnecté.e.", "success")
            return redirect(url_for('auth.login'))

        # TODO: Pour toute autre méthode HTTP, refuser la requête avec message et rediriger
        flash("Méthode non autorisée", "danger")
        return redirect(url_for('auth.login'))



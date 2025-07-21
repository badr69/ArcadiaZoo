from flask import render_template, request, jsonify
from app.models.user_model import UserModel
from app.forms.auth_forms import LoginForm
from flask_login import login_user, logout_user
from flask import redirect, url_for, flash
from app.utils.security import verify_password

class AuthController:
    @staticmethod
    def login():
        form = LoginForm()

        # On détecte si c'est une requête AJAX ou non
        is_fetch = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        if request.method == 'POST':
            if form.validate_on_submit():
                user = UserModel.get_by_email(form.email.data)

                if user and verify_password(user.password_hash, form.password.data):
                    login_user(user)

                    # En mode fetch() → on renvoie du JSON
                    if is_fetch:
                        # Redirection cible selon rôle
                        if user.role_name == 'admin':
                            return jsonify({"success": True, "redirect": url_for('admin.admin_dash')})
                        elif user.role_name == 'employee':
                            return jsonify({"success": True, "redirect": url_for('employee.employee_dash')})
                        elif user.role_name == 'vet':
                            return jsonify({"success": True, "redirect": url_for('vet.vet_dash')})
                        else:
                            return jsonify({"success": False, "message": "Rôle inconnu"}), 400

                    # Sinon → requête HTML normale
                    flash(f"Bienvenue {user.username} !", "success")
                    if user.role_name == 'admin':
                        return redirect(url_for('admin.admin_dash'))
                    elif user.role_name == 'employee':
                        return redirect(url_for('employee.employee_dash'))
                    elif user.role_name == 'vet':
                        return redirect(url_for('vet.vet_dash'))

                else:
                    # Mauvais identifiants
                    if is_fetch:
                        return jsonify({"success": False, "message": "Email ou mot de passe incorrect"}), 401
                    flash("Email ou mot de passe incorrect", "danger")
                    return redirect(url_for('auth.login'))

            else:
                # Form invalide
                if is_fetch:
                    return jsonify({"success": False, "errors": form.errors}), 400
                flash("Formulaire invalide", "danger")
                return redirect(url_for('auth.login'))

        # GET → on affiche le formulaire normalement
        return render_template('auth/login.html', form=form)

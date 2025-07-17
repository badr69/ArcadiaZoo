from flask import redirect, url_for, flash, render_template, request
from app.models.user_model import UserModel
from app.forms.auth_forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from flask import redirect, url_for, flash
from app.utils.security import hash_password, verify_password

print("🧩 Méthode login() de AuthController appelée")

class AuthController:
    @staticmethod
    def login():
        form = LoginForm()

        if request.method == 'POST':
            print("➡️ Form POST reçu")
            print("Email:", form.email.data)
            print("Password:", form.password.data)

        if form.validate_on_submit():
            print("✅ Formulaire validé")

            user = UserModel.get_by_email(form.email.data)
            print("Utilisateur trouvé:", user)

            if user and verify_password(user.password_hash, form.password.data):
                print("✅ Mot de passe correct")
                login_user(user)
                print("🔐 Utilisateur connecté :", user.username)
                flash(f'Bienvenue {user.username} !', 'success')

                if user.role_name == 'admin':
                    print("➡️ Redirection vers admin_dash")
                    return redirect(url_for('admin.admin_dash'))
                elif user.role_name == "employee":
                    print("➡️ Redirection vers employee_dash")
                    return redirect(url_for('employee.employee_dash'))
                elif user.role_name == "vet":
                    print("➡️ Redirection vers vet_dash")
                    return redirect(url_for('vet.vet_dash'))
                else:
                    print("❌ Rôle non reconnu :", user.role_name)
                    flash("Rôle non reconnu.", "danger")
                    return redirect(url_for('auth.login'))

            else:
                print("❌ Email ou mot de passe incorrect")
                flash("Email ou mot de passe incorrect.", "danger")
                return redirect(url_for('auth.login'))

        print("❌ Formulaire invalide ou méthode GET")
        return render_template('auth/login.html', form=form)



    # @app.route('/logout')
    # @login_required
    @staticmethod
    def logout():
        logout_user()
        flash("You are diconected.", "success")
        return redirect(url_for('index'))

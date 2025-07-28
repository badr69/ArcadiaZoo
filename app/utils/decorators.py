from functools import wraps
from flask import redirect, url_for, flash, request
from flask_login import current_user, login_required

def admin_required(f):
    """Autorise uniquement les Admins."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        # Évite la boucle si on est déjà sur /auth/login
        if request.endpoint == 'auth.login':
            return f(*args, **kwargs)

        if current_user.role != "admin":
            flash("Accès réservé aux administrateurs.", "danger")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return decorated_function


def roles_required(*roles):
    """Autorise plusieurs rôles (ex: admin ou vet)."""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            # Évite la boucle si on est déjà sur /auth/login
            if request.endpoint == 'auth.login':
                return f(*args, **kwargs)

            if current_user.role not in roles:
                flash("Vous n’avez pas les permissions nécessaires.", "danger")
                return redirect(url_for("main.home"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Préconfigurations pratiques
admin_or_vet_required = roles_required("admin", "vet")
admin_or_employee_required = roles_required("admin", "employee")
admin_or_employee_or_vet_required = roles_required("admin", "employee", "vet")

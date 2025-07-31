from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"DEBUG: current_user.is_authenticated={current_user.is_authenticated}, role_name={getattr(current_user, 'role_name', None)}")

        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))  # Redirection vers login
        if current_user.role_name != "admin":
            abort(403)  # Si connecté mais pas admin
        return f(*args, **kwargs)
    return decorated_function


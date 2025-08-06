from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)  # Non connecté
            if current_user.role not in roles:
                abort(403)  # Pas le bon rôle
            return f(*args, **kwargs)
        return decorated_function
    return decorator



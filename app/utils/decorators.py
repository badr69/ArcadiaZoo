from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = getattr(current_user, 'role_name', None)
            print(f"DEBUG — current_user: {current_user.username}, role_name: {user_role}")
            if user_role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# def roles_required(*roles):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if not current_user.is_authenticated:
#                 abort(401)  # Non connecté
#             if current_user.role not in roles:
#                 abort(403)  # Pas le bon rôle
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator
#


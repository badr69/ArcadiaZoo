from wtforms.validators import ValidationError
import re

def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_strong_password(password: str) -> bool:
    # Min 8 chars, au moins 1 majuscule, 1 chiffre, 1 caractère spécial
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$'
    return re.match(pattern, password) is not None

def is_safe_input(user_input: str) -> bool:
    pattern = r"(--|;|'|\"|/\*|\*/|xp_)"
    return re.match(pattern, user_input) is not None




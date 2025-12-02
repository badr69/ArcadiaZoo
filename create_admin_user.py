# create_admin_user.py
import sys
from werkzeug.security import generate_password_hash
from app.models.user_model import UserModel
from app.models.role_model import RoleModel

def create_admin(username: str, email: str, password: str):
    user_model = UserModel()
    role_model = RoleModel()

    # Vérifie si l'utilisateur existe déjà
    existing_user = user_model.get_user_by_email(email)
    if existing_user:
        print(f"Utilisateur avec email '{email}' existe déjà.")
        return

    # Vérifie si le rôle admin existe, sinon le crée
    admin_role = next((r for r in role_model.list_all_roles() if r.name.lower() == "admin"), None)
    if not admin_role:
        role_model.create_role("admin")
        admin_role = next((r for r in role_model.list_all_roles() if r.name.lower() == "admin"), None)

    # Crée l'utilisateur avec mot de passe haché
    password_hash = generate_password_hash(password)
    success = user_model.create_user(username=username, email=email, password_hash=password_hash, role_id=admin_role.role_id)

    if success:
        print(f"Utilisateur admin '{username}' créé avec succès !")
    else:
        print("Erreur lors de la création de l'utilisateur admin.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_admin_user.py <username> <email> <password>")
    else:
        create_admin(sys.argv[1], sys.argv[2], sys.argv[3])

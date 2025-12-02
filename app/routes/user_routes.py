from app.controllers.user_controller import UserController
from flask import Blueprint
from app.utils.decorators import roles_required
from flask_login import login_required

user_bp = Blueprint('user', __name__, url_prefix='/user')


# -------------------- LIST --------------------
@user_bp.route('/list_all_users', methods=['GET'])
@login_required
@roles_required("admin")
def list_all_users():
    # Méthode statique -> pas besoin d'instance
    return UserController.list_all_users()


# -------------------- GET BY ID --------------------
@user_bp.route('/<int:user_id>', methods=['GET'])
@login_required
@roles_required("admin")
def get_user_by_id(user_id):
    # Méthode statique -> pas besoin d'instance
    return UserController.get_user_by_id(user_id)

# -------------------- CREATE --------------------
@user_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
@roles_required("admin")
def create_user():
    # Méthode statique -> pas besoin d'instance
    return UserController.create_user()


# -------------------- UPDATE --------------------
@user_bp.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@roles_required("admin")
def update_user(user_id):
    # Méthode d'instance -> on instancie avec user_id
    controller = UserController(user_id)
    return controller.update_user()


# -------------------- DELETE --------------------
@user_bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@roles_required("admin")
def delete_user(user_id):
    # Méthode d'instance -> on instancie avec user_id
    controller = UserController(user_id)
    return controller.delete_user()




from flask import Blueprint
from app.controllers.food_controller import FoodController
from app.utils.decorators import roles_required

food_bp = Blueprint('food', __name__, url_prefix='/food')

@food_bp.route('/list_all_foods', methods=['GET'])
@roles_required("admin", "employee", "vet")
def list_all_foods():
    return FoodController.list_all_foods()  # méthode statique OK

@food_bp.route('/<int:food_id>', methods=['GET'])
@roles_required("admin", "employee", "vet")
def get_food_by_id(food_id):
    controller = FoodController(food_id)
    return controller.get_food_by_id()

@food_bp.route('/create_food', methods=['GET', 'POST'])
@roles_required("admin", "employee", "vet")
def create_food():
    # Méthode statique de création, pas besoin d'instance
    return FoodController.create_food()

@food_bp.route('/update_food/<int:food_id>', methods=['GET', 'POST'])
@roles_required("admin", "employee", "vet")
def update_food(food_id):
    controller = FoodController(food_id)
    return controller.update_food()

@food_bp.route('/delete_food/<int:food_id>', methods=['POST'])
@roles_required("admin", "employee", "vet")
def delete_food(food_id):
    controller = FoodController(food_id)
    return controller.delete_food()

@food_bp.route('/debug_role')
def debug_role():
    from flask_login import current_user
    return {
        "username": getattr(current_user, "username", None),
        "role": getattr(current_user, "role", None),
        "role_name": getattr(current_user, "role_name", None)
    }

from flask import Blueprint
from app.controllers.food_controller import FoodController
from app.utils.decorators import roles_required

food_bp = Blueprint('food', __name__, url_prefix='/food')

@food_bp.route('/list_all_foods', methods=['GET'])
@roles_required("admin", "employee")
def list_all_foods():
    return FoodController.list_all_foods()

@food_bp.route('/<int:food_id>', methods=['GET'])
@roles_required("admin", "employee")
def get_food_by_id(food_id):
    return FoodController.get_food_by_id(food_id)

@food_bp.route('/create_food', methods=['GET', 'POST'])
@roles_required("admin", "employee")
def create_food():
    return FoodController.create_food()

@food_bp.route('/update_food/<int:food_id>', methods=['GET', 'POST'])
@roles_required("admin", "employee")
def update_food(food_id):
    return FoodController.update_food(food_id)

@food_bp.route('/delete_food/<int:food_id>', methods=['POST'])
@roles_required("admin", "employee")
def delete_food(food_id):
    return FoodController.delete_food(food_id)

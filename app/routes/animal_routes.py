from flask import Blueprint
from app.controllers.animal_controller import AnimalController
from app.utils.decorators import roles_required

animal_bp = Blueprint('animal', __name__, url_prefix="/animal")


@animal_bp.route('/list_all_animals', methods=['GET'])
@roles_required('admin', 'employee')
def list_all_animals():
    return AnimalController.list_all_animals()

@animal_bp.route('/create_animal', methods=['GET', 'POST'])
@roles_required('admin')
def create_animal():
    return AnimalController.create_animal()

@animal_bp.route('/<int:animal_id>', methods=['GET'])
@roles_required('admin', 'employee')
def get_animal_by_id(animal_id):
    return AnimalController.get_animal_by_id(animal_id)

@animal_bp.route('/update_animal/<int:animal_id>', methods=['GET', 'POST'])
@roles_required('admin', 'employee')
def update_animal(animal_id):
    return AnimalController.update_animal(animal_id)

@animal_bp.route('/<int:animal_id>/delete', methods=['POST'])
@roles_required('admin', 'employee')
def delete_animal(animal_id):
    return AnimalController.delete_animal(animal_id)

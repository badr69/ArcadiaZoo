from flask import Blueprint
from app.controllers.animal_controller import AnimalController
from flask_login import login_required

animal_bp = Blueprint('animal', __name__, url_prefix="/animal")


@animal_bp.route('/list_all_animals', methods=['GET'])

def list_all_animals():
    return AnimalController.list_all_animals()

@animal_bp.route('/create_animal', methods=['GET', 'POST'])

def create_animal():
    return AnimalController.create_animal()

@animal_bp.route('/<int:animal_id>', methods=['GET'])

def get_animal_by_id(animal_id):
    return AnimalController.get_animal_by_id(animal_id)

@animal_bp.route('/update_animal/<int:animal_id>', methods=['GET', 'POST'])

def update_animal(animal_id):
    return AnimalController.update_animal(animal_id)

@animal_bp.route('/<int:animal_id>/delete', methods=['POST'])

def delete_animal(animal_id):
    return AnimalController.delete_animal(animal_id)

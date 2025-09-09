from flask import Blueprint
from app.controllers.animal_click_controller import AnimalClickController

animal_click_bp = Blueprint('animal_click', __name__, url_prefix='/animal_clicks')



@animal_click_bp.route('/<int:animal_id>/click', methods=['POST'])
def add_click(animal_id):
    return AnimalClickController.add_click(animal_id)

@animal_click_bp.route('/<int:animal_id>/total', methods=['GET'])
def get_total_clicks(animal_id):
    return AnimalClickController.get_total_clicks(animal_id)

@animal_click_bp.route('/<int:animal_id>/by_date', methods=['GET'])
def get_clicks_by_date(animal_id):
    return AnimalClickController.get_clicks_by_date(animal_id)

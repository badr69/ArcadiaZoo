from flask import Blueprint
from app.controllers.habitat_controller import HabitatController
from app.utils.decorators import admin_required

habitat_bp = Blueprint('habitat', __name__, url_prefix="/habitat")


@habitat_bp.route('/list_all_habitats', methods=['GET'])
@admin_required
def list_all_habitats():
    return HabitatController.list_all_habitats()

@habitat_bp.route('/create_habitat', methods=['GET', 'POST'])
@admin_required
def create_habitat():
    return HabitatController.create_habitat()

@habitat_bp.route('/<int:habitat_id>', methods=['GET'])
@admin_required
def get_habitat_by_id(habitat_id):
    return HabitatController.get_habitat_by_id(habitat_id)

@habitat_bp.route('/update_habitat/<int:habitat_id>', methods=['GET', 'POST'])
@admin_required
def update_habitat(habitat_id):
    return HabitatController.update_habitat(habitat_id)

@habitat_bp.route('/delete_habitat/<int:habitat_id>', methods=['POST'])
@admin_required
def delete_habitat(habitat_id):
    return HabitatController.delete_habitat(habitat_id)

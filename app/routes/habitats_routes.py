from flask import Blueprint
from app.controllers.habitat_controller import HabitatController
from app.utils.decorators import roles_required

habitat_bp = Blueprint('habitat', __name__, url_prefix="/habitat")


@habitat_bp.route('/list_all_habitats', methods=['GET'])
@roles_required("admin")
def list_all_habitats():
    return HabitatController.list_all_habitats()


@habitat_bp.route('/create_habitat', methods=['GET', 'POST'])
@roles_required("admin")
def create_habitat():
    return HabitatController.create_habitat()


@habitat_bp.route('/<int:habitat_id>', methods=['GET'])
@roles_required("admin")
def get_habitat_by_id(habitat_id):
    return HabitatController.get_habitat_by_id(habitat_id)


@habitat_bp.route('/update_habitat/<int:habitat_id>', methods=['GET', 'POST'])
@roles_required("admin")
def update_habitat(habitat_id):
    controller = HabitatController(habitat_id)  # instanciation avec l'ID
    return controller.update_habitat()          # appel de la méthode d'instance


@habitat_bp.route('/delete_habitat/<int:habitat_id>', methods=['POST'])
@roles_required("admin")
def delete_habitat(habitat_id):
    controller = HabitatController(habitat_id)  # instanciation avec l'ID
    return controller.delete_habitat()          # appel de la méthode d'instance

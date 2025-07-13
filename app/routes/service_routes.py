from flask import Blueprint
from app.controllers.service_controller import ServiceController


service_bp = Blueprint('service', __name__, url_prefix="/service")


@service_bp.route('/list_all_services', methods=['GET'])
def list_all_services():
    return ServiceController.list_all_services()

@service_bp.route('/create_service', methods=['GET', 'POST'])
def create_service():
    return ServiceController.create_service()

@service_bp.route('/<int:service_id>', methods=['GET'])
def get_service_by_id(service_id):
    return ServiceController.get_service_by_id(service_id)

@service_bp.route('/update_service/<int:service_id>', methods=['GET', 'POST'])
def update_service(service_id):
    return ServiceController.update_service(service_id)

@service_bp.route('/<int:service_id>/delete', methods=['POST'])
def delete_service(service_id):
    return ServiceController.delete_service(service_id)

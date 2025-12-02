from flask import Blueprint
from app.controllers.service_controller import ServiceController
from app.utils.decorators import roles_required

service_bp = Blueprint('service', __name__, url_prefix="/service")

@service_bp.route('/list_all_services', methods=['GET'])
@roles_required("admin", "employee")
def list_all_services():
    return ServiceController.list_all_services()

@service_bp.route('/create_service', methods=['GET', 'POST'])
@roles_required("admin", "employee")
def create_service():
    return ServiceController.create_service()

@service_bp.route('/<int:service_id>', methods=['GET'])
@roles_required("admin", "employee")
def get_service_by_id(service_id):
    return ServiceController.get_service_by_id(service_id)

@service_bp.route('/update_service/<int:service_id>', methods=['GET', 'POST'])
@roles_required("admin", "employee")
def update_service(service_id):
    controller = ServiceController(service_id)
    return controller.update_service()

@service_bp.route('/delete_service/<int:service_id>', methods=['POST'])
@roles_required("admin", "employee")
def delete_service(service_id):
    controller = ServiceController(service_id)
    return controller.delete_service()

from flask import Blueprint
from app.controllers.img_habitat_controller import ImgHabitatController
from app.utils.decorators import admin_required

img_habitat_bp = Blueprint('img_habitat', __name__)

@img_habitat_bp.route('/list', methods=['GET'])
# @admin_required
def get_all():
    return ImgHabitatController.get_all()

@img_habitat_bp.route('/create', methods=['GET', 'POST'])
# @admin_required
def create():
    return ImgHabitatController.create()

@img_habitat_bp.route('/<int:id>', methods=['GET'])
# @admin_required
def get_by_id(id):
    return ImgHabitatController.get_by_id(id)

@img_habitat_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def edit(id):
    return ImgHabitatController.update(id)

@img_habitat_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    return ImgHabitatController.delete(id)

# from flask import Blueprint
# from flask_login import login_required
# from app.controllers.img_habitat_controller import ImgHabitatController
# from app.utils.decorators import roles_required
#
# img_habitat_bp = Blueprint('img_habitat', __name__, url_prefix="/img_habitat")
#
# @img_habitat_bp.route('/list_all_img_ha', methods=['GET'])
# @login_required
# @roles_required("admin")
# def list_all_img_ha():
#     return ImgHabitatController.list_all_img_ha()
#
# @img_habitat_bp.route('/<int:img_ha_id>', methods=['GET'])
# @login_required
# @roles_required("admin")
# def get_img_ha_by_id(img_ha_id):
#     controller = ImgHabitatController(img_ha_id)
#     return controller.get_img_ha_by_id()
#
# @img_habitat_bp.route('/create_img_habitat', methods=['GET', 'POST'])
# @login_required
# @roles_required("admin")
# def create_img_habitat():
#     return ImgHabitatController.create_img_habitat()
#
# @img_habitat_bp.route('/update_img_habitat/<int:img_ha_id>', methods=['GET', 'POST'])
# @login_required
# @roles_required("admin")
# def update_img_habitat(img_ha_id):
#     controller = ImgHabitatController(img_ha_id)
#     return controller.update_img_habitat()
#
# @img_habitat_bp.route('/delete_img_habitat/<int:img_ha_id>', methods=['POST'])
# @login_required
# @roles_required("admin")
# def delete_img_habitat(img_ha_id):
#     controller = ImgHabitatController(img_ha_id)
#     return controller.delete_img_habitat()

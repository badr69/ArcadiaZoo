# from flask import Blueprint
# from app.controllers.img_habitat_controller import ImgHabitatController
# from app.utils.decorators import admin_required
#
# img_habitat_bp = Blueprint('img_habitat', __name__, url_prefix="/img_habitat")
#
# @img_habitat_bp.route('/list_all_ha_img', methods=['GET'])
# @admin_required
# def list_all_ha_img():
#     return ImgHabitatController.list_all_ha_img()
#
# @img_habitat_bp.route('/<int:id>', methods=['GET'])
# @admin_required
# def get_ha_img_by_id(img_ha_id):
#     return ImgHabitatController.get_ha_img_by_id(img_ha_id)
#
# @img_habitat_bp.route('/create_ha_img', methods=['GET', 'POST'])
# @admin_required
# def create_ha_img():
#     return ImgHabitatController.create_ha_img()
#
# @img_habitat_bp.route('/update_ha_img/<int:id>', methods=['GET', 'POST'])
# @admin_required
# def update_ha_img(img_ha_id):
#     return ImgHabitatController.update_ha_img(img_ha_id)
#
# @img_habitat_bp.route('/delete_ha_img/<int:id>', methods=['POST'])
# @admin_required
# def delete_ha_img(img_ha_id):
#     return ImgHabitatController.delete_ha_img(img_ha_id)

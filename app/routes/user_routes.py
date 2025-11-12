from app.controllers.user_controller import UserController
from flask import Blueprint
from app.utils.decorators import roles_required
from flask_login import login_required


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
@roles_required("admin")
def create_user():
    controller = UserController()
    return controller.create_user()

@user_bp.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@roles_required("admin")
def update_user(user_id):
    controller = UserController()
    return controller.update_user(user_id)

@user_bp.route('/delete_user/<int:user_id>', methods=['GET','POST'])
@login_required
@roles_required("admin")
def delete_user(user_id):
    controller = UserController()
    return controller.delete_user(user_id)

@user_bp.route('/list_all_users', methods=['GET'])
@login_required
@roles_required("admin")
def list_all_users():
    return UserController.list_all_users()  # classmethod, pas besoin d'instance

@user_bp.route('/<int:user_id>', methods=['GET'])
@login_required
@roles_required("admin")
def get_user_by_id(user_id):
    return UserController.get_user_by_id(user_id)  # classmethod




# from flask import Blueprint, render_template,abort
#
# from app.controllers.care_controller import CareController
# from app.controllers.user_controller import UserController
# from app.utils.decorators import roles_required
#
#
# user_bp = Blueprint('user', __name__, url_prefix="/user")
#
# @user_bp.route("/list_all_users")
# @roles_required("admin")
# def list_all_users():
#      return UserController.list_all_users()
#
# # Lister tous les vets
# @user_bp.route("/list_all_vets", methods=["GET"])
# @roles_required("admin", "vet")
# def list_all_vets():
#     return CareController.list_all_vets()
#
# @user_bp.route("/<int:user_id>")
# @roles_required("admin")
# def get_user_by_id(user_id):
#     user = UserController.get_user_by_id(user_id)
#     if not user:
#         abort(404)  # renvoie une erreur 404 si l'utilisateur n'existe pas
#     return render_template("user/user_detail.html", user=user)
#
# @user_bp.route("/create_user", methods=["GET", "POST"])
# @roles_required("admin")
# def create_user():
#     return UserController.create_user()
#
# @user_bp.route("/update_user/<int:user_id>", methods=["GET", "POST"])
# @roles_required("admin")
# def update_user(user_id):
#     return UserController.update_user(user_id)
#
# @user_bp.route("/delete_user/<int:user_id>", methods=["POST"])
# @roles_required("admin")
# def delete_user(user_id):
#     return UserController.delete_user(user_id)
#

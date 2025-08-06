from flask import Blueprint, render_template,abort
from app.controllers.user_controller import UserController
from app.utils.decorators import roles_required


user_bp = Blueprint('user', __name__, url_prefix="/user")

@user_bp.route("/list_all_users")
@roles_required("admin")
def list_all_users():
     return UserController.list_all_users()

@user_bp.route("/<int:user_id>")
@roles_required("admin")
def get_user_by_id(user_id):
    user = UserController.get_user_by_id(user_id)
    if not user:
        abort(404)  # renvoie une erreur 404 si l'utilisateur n'existe pas
    return render_template("user/user_detail.html", user=user)

@user_bp.route("/create_user", methods=["GET", "POST"])
@roles_required("admin")
def create_user():
    return UserController.create_user()

@user_bp.route("/update_user/<int:user_id>", methods=["GET", "POST"])
@roles_required("admin")
def update_user(user_id):
    return UserController.update_user(user_id)

@user_bp.route("/delete_user/<int:user_id>", methods=["POST"])
@roles_required("admin")
def delete_user(user_id):
    return UserController.delete_user(user_id)


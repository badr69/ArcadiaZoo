from flask import Blueprint, render_template,abort
from app.controllers.user_controller import UserController
from app.utils.decorators import admin_required



user_bp = Blueprint('user', __name__, url_prefix="/user")


@user_bp.route("/list_all_users")
@admin_required
def list_all_users():
     return UserController.list_all_users()

@user_bp.route("/<int:user_id>")
@admin_required
def get_user_by_id(user_id):
    user = UserController.get_user_by_id(user_id)
    if not user:
        abort(404)  # renvoie une erreur 404 si l'utilisateur n'existe pas
    return render_template("user/user_detail.html", user=user)

@user_bp.route("/create_user", methods=["GET", "POST"])
@admin_required
def create_user():
    return UserController.create_user()

@user_bp.route("/update_user/<int:user_id>", methods=["GET", "POST"])
@admin_required
def update_user(user_id):
    return UserController.update_user(user_id)

@user_bp.route("/delete_user/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    return UserController.delete_user(user_id)


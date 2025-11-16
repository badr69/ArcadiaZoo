# from flask import Blueprint
# from app.controllers.care_controller import CareController
# from app.utils.decorators import roles_required
#
# # Blueprint pour les pages HTML classiques
# care_bp = Blueprint("care", __name__, url_prefix="/care")
#
# # -------------------------------
# # Routes HTML CRUD
# # -------------------------------
#
# # 🧩 Créer un care
# @care_bp.route("/create_care", methods=["GET", "POST"])
# @roles_required("admin", "vet")
# def create_care():
#     return CareController.create_care()
#
# # 🧩 Lister tous les cares
# @care_bp.route("/list_all_cares", methods=["GET"])
# @roles_required("admin", "vet")
# def list_all_cares():
#     return CareController.list_all_cares()
#
#
#
# # 🧩 Voir le détail d’un care
# @care_bp.route("/<int:care_id>", methods=["GET"])
# @roles_required("admin", "vet")
# def get_care_by_id(care_id):
#     return CareController.get_care_by_id(care_id)
#     # Si tu veux afficher un template : render_template("care/detail_care.html", care=care)
#
# # 🧩 Modifier un care
# @care_bp.route("/edit/<int:care_id>", methods=["GET", "POST"])
# @roles_required("admin", "vet")
# def update_care(care_id):
#     return CareController.update_care(care_id)
#
# # 🧩 Supprimer un care
# @care_bp.route("/delete/<int:care_id>", methods=["POST"])
# @roles_required("admin", "vet")
# def delete_care(care_id):
#     return CareController.delete_care(care_id)
#
# # -------------------------------
# # Routes API (JSON / AJAX / Fetch)
# # -------------------------------
# api_bp = Blueprint("care_api", __name__, url_prefix="/api/care")
#
# # Lister tous les cares en JSON
# api_bp.route("/list_all_cares", methods=["GET"])(CareController.api_list_all_cares)
#
#
#
#
#

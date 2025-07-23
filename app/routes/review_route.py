from flask import Blueprint, request, jsonify
from app.controllers.review_controller import ReviewController

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

# Route POST appelée par fetch (JS)
@reviews_bp.route('/submit_review', methods=['POST'])
def submit_review():
    return ReviewController.submit_review()


@reviews_bp.route('/add', methods=['POST'])
def add_review():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Pas de données reçues"}), 400
    try:
        review_id = ReviewController.add_review(data)
        return jsonify({"message": "Avis ajouté avec succès", "id": review_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Erreur serveur"}), 500




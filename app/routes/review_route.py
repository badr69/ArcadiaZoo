from flask import Blueprint
from app.controllers.review_controller import ReviewController

reviews_bp = Blueprint('reviews_bp', __name__, url_prefix='/reviews')

reviews_bp.route('/add_review', methods=['POST'])(ReviewController.add_review)
reviews_bp.route('/get_all_reviews', methods=['GET'])(ReviewController.get_all_reviews)
reviews_bp.route('/list_all_reviews', methods=['GET'])(ReviewController.list_all_reviews)
reviews_bp.route('/<string:review_id>', methods=['GET'])(ReviewController.get_review_by_id)
reviews_bp.route('/element/<string:element_id>', methods=['GET'])(ReviewController.get_reviews_by_element_id)


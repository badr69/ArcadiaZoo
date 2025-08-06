from flask import Blueprint
from app.controllers.review_controller import ReviewController


reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@reviews_bp.route('/add_review', methods=['POST'])
def add_review():
    return ReviewController.add_review()

@reviews_bp.route('/get_all_reviews', methods=['GET'])
def get_all_reviews():
    return ReviewController.get_all_reviews()

@reviews_bp.route('/<string:review_id>', methods=['GET'])
def get_review_by_id(review_id):
    return ReviewController.get_review_by_id(review_id)

@reviews_bp.route('/element/<string:element_id>', methods=['GET'])
def get_review_by_element_id(element_id):
    return ReviewController.get_review_by_element_id(element_id)

@reviews_bp.route('/published', methods=['GET'])
def get_published_reviews():
    return ReviewController.get_published_reviews()

@reviews_bp.route('/publish/<string:review_id>', methods=['PATCH'])
def publish_review(review_id):
    return ReviewController.publish_review(review_id)

@reviews_bp.route('/delete/<string:review_id>', methods=['DELETE'])
def delete_review(review_id):
    return ReviewController.delete_review(review_id)


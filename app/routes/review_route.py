from flask import Blueprint, render_template, jsonify
from app.controllers.review_controller import ReviewController
from app.models.review_model import Review

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@reviews_bp.route('/submit_review', methods=['POST'])
def submit_review():
    return ReviewController.submit_review()

@reviews_bp.route('/list_all_reviews', methods=['GET'])
def list_all_reviews():
    reviews = Review.get_all()
    return render_template('index.html', reviews=reviews)

@reviews_bp.route('/get_all', methods=['GET'])
def get_all_reviews():
    try:
        reviews = Review.get_all()
        return jsonify(reviews), 200
    except Exception as e:
        print("Erreur récupération reviews :", e)
        return jsonify([]), 500





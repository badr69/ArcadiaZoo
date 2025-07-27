from flask import Blueprint, render_template
from app.controllers.review_controller import ReviewController

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

# Route POST utilisée par fetch (JS) ou formulaire HTML
@reviews_bp.route('/submit_review', methods=['POST'])
def submit_review():
    return ReviewController.submit_review()

# Route GET pour afficher la page avec tous les reviews
@reviews_bp.route('/list_all_eviews', methods=['GET'])
def list_all_reviews():
    reviews = ReviewController.get_all()
    return render_template('index.html', reviews=reviews)

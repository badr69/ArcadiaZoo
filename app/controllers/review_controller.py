from flask import request, jsonify
from app.models.review_model import ReviewModel

class ReviewController:

    @staticmethod
    def add_review():
        data = request.get_json()
        try:
            review_id = ReviewModel.add_review(data)
            return jsonify({"status": "success", "review_id": review_id}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    @staticmethod
    def get_all_reviews():
        reviews = ReviewModel.get_all_reviews()
        reviews_dict = [r.to_dict() for r in reviews]
        return jsonify(reviews_dict), 200

    @staticmethod
    def get_review_by_id(review_id):
        review = ReviewModel.get_review_by_id(review_id)
        if review:
            return jsonify(review.to_dict()), 200
        else:
            return jsonify({"status": "error", "message": "Review not found"}), 404

    @staticmethod
    def get_review_by_element_id(element_id):
        reviews = ReviewModel.get_review_by_element_id(element_id)
        reviews_dict = [r.to_dict() for r in reviews]
        return jsonify(reviews_dict), 200

    @staticmethod
    def get_published_reviews():
        reviews = ReviewModel.get_published_reviews()
        reviews_dict = [r.to_dict() for r in reviews]
        return jsonify(reviews_dict), 200

    @staticmethod
    def publish_review(review_id):
        success = ReviewModel.publish_review(review_id)
        if success:
            return jsonify({"status": "success", "message": "Review published"}), 200
        else:
            return jsonify({"status": "error", "message": "Review not found or not updated"}), 404

    @staticmethod
    def delete_review(review_id):
        success = ReviewModel.delete_review(review_id)
        if success:
            return jsonify({"status": "success", "message": "Review deleted"}), 200
        else:
            return jsonify({"status": "error", "message": "Review not found"}), 404


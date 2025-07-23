from flask import request, jsonify
from datetime import datetime
from app.db.mongo import db

reviews_collection = db["reviews"]

class ReviewController:

    @staticmethod
    def add_review(data):
        pseudo = data.get("pseudo")
        message = data.get("message")
        rating = data.get("rating")


        if not all([pseudo, message, rating]):
            raise ValueError("Champs manquants")

        review = {
            "pseudo": pseudo,
            "message": message,
            "rating": int(rating),
            "date": datetime.utcnow()
        }

        result = reviews_collection.insert_one(review)
        return str(result.inserted_id)

    @staticmethod
    def submit_review():
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Données manquantes"}), 400

            review_id = ReviewController.add_review(data)
            return jsonify({"message": "Avis envoyé avec succès", "id": review_id}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            print(f"Erreur serveur: {e}")
            return jsonify({"error": "Erreur serveur"}), 500

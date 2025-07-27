from flask import request, jsonify
from datetime import datetime
from app.db.mongo import reviews_collection


class ReviewController:

    @staticmethod
    def submit_review():
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Données manquantes"}), 400

            pseudo = data.get("pseudo")
            message = data.get("message")
            rating = data.get("rating")
            if not all([pseudo, message, rating]):
                return jsonify({"error": "Champs manquants"}), 400

            review = {
                "pseudo": pseudo,
                "message": message,
                "rating": int(rating),
                "element_id": "global",  # ou autre élément selon contexte
                "date": datetime.utcnow()
            }
            result = reviews_collection.insert_one(review)

            review["_id"] = str(result.inserted_id)
            review["date"] = review["date"].isoformat()

            return jsonify(review), 201

        except Exception as e:
            print(f"Erreur serveur: {e}")
            return jsonify({"error": "Erreur serveur"}), 500

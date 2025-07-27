from flask import request, jsonify
from datetime import datetime
from app.db.mongo import db
from app.models.review_model import Review
reviews_collection = db["reviews"]

class ReviewController:

    @staticmethod
    def add_review(data):
        print("Données reçues par add_review:", data, type(data))
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
            print("Contenu brut :", request.data)
            print("Content-Type :", request.headers.get("Content-Type"))
            data = request.get_json()
            print("Données reçues :", data)
            if not data:
                return jsonify({"error": "Données manquantes"}), 400

            review_id = ReviewController.add_review(data)
            return jsonify({"message": "Avis envoyé avec succès", "id": review_id}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            print(f"Erreur serveur: {e}")
            return jsonify({"error": "Erreur serveur"}), 500

    @staticmethod
    def get_all():
        reviews = Review.get_all()
        review_dicts = []

        for review in reviews:
            review_data = review.to_dict()
            # JSON-ready: convertir date et _id
            review_data["_id"] = str(review._id) if review._id else None
            review_data["date"] = review_data["date"].isoformat() if review_data.get("date") else None
            review_dicts.append(review_data)

        return jsonify(review_dicts)

    #
    # @staticmethod
    # def get_all_reviews():
    #     # Récupérer tous les reviews, avec les champs utiles + _id, triés par date décroissante
    #     reviews = list(
    #         reviews_collection.find({}, {'pseudo': 1, 'message': 1, 'rating': 1, 'date': 1, 'element_id': 1}).sort(
    #             "date", -1))
    #
    #     # Convertir _id et date en formats sérialisables JSON
    #     for review in reviews:
    #         review['_id'] = str(review['_id'])
    #         if 'date' in review and review['date']:
    #             review['date'] = review['date'].isoformat()
    #
    #     return jsonify(reviews)

    # reviews
    # @staticmethod
    # def get_reviews():
    #     # récupère toutes les reviews triées par date décroissante
    #     reviews_cursor = reviews_collection.find().sort("date", -1)
    #     reviews = []
    #     for review in reviews_cursor:
    #         # Convertir l'_id MongoDB en string et la date au format lisible
    #         review["_id"] = str(review["_id"])
    #         review["date"] = review["date"].isoformat() if review["date"] else None
    #         reviews.append(review)
    #     return reviews

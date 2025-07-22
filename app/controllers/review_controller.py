from datetime import datetime
from app.db.mongo import db

reviews_collection = db["reviews"]

class ReviewController:

    @staticmethod
    def add_review(data):
        pseudo= data.get("pseudo")
        message = data.get("message")
        rating = data.get("rating")
        element_id = data.get("element_id")

        if not all([pseudo, message, rating, element_id]):
            raise ValueError("Champs manquants")

        review = {
            "pseudo": pseudo,
            "message": message,
            "rating": int(rating),
            "element_id": element_id,
            "date": datetime.utcnow()
        }

        result = reviews_collection.insert_one(review)
        return str(result.inserted_id)

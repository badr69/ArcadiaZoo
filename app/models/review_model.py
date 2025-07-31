from datetime import datetime
from app.db.mongo import db
from bson import ObjectId

reviews_collection = db["reviews"]


class ReviewModel:
    def __init__(self, pseudo, message, rating, element_id=None, date=None, _id=None,  published=False):
        self.id = str(_id) if _id else None
        self.pseudo = pseudo
        self.message = message
        self.rating = int(rating)
        self.element_id = element_id
        self.published = published
        self.date = date if date else datetime.now()


    @staticmethod
    def from_dict(data):
        return ReviewModel(
            pseudo=data.get("pseudo"),
            message=data.get("message"),
            rating=data.get("rating"),
            element_id=data.get("element_id"),
            date=data.get("date"),
            published=data.get("published", False),
            _id=data.get("_id")
        )

    def to_dict(self):
        return {
            "id": self.id,
            "pseudo": self.pseudo,
            "message": self.message,
            "rating": self.rating,
            "element_id": self.element_id,
            "date": self.date.isoformat() if self.date else None,
            "published": self.published
        }

    @staticmethod
    def add_review(data):
        pseudo = data.get("pseudo")
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
            "date": datetime.utcnow(),
            "published": False
        }
        try:
            result = reviews_collection.insert_one(review)
            print("Insertion réussie, ID :", result.inserted_id)
            return str(result.inserted_id)
        except Exception as e:
            print("Erreur insertion MongoDB :", e)
            raise

    @staticmethod
    def get_all_reviews():
        try:
            reviews = reviews_collection.find().sort("date", -1)
            return [ReviewModel.from_dict(r) for r in reviews]
        except Exception as e:
            print(f"Erreur get_all_reviews: {e}")
            return []

    @staticmethod
    def get_review_by_id(review_id):
        try:
            review = reviews_collection.find_one({"_id": ObjectId(review_id)})
            if not review:
                return None
            return ReviewModel.from_dict(review)
        except Exception as e:
            print(f"Erreur get_by_id: {e}")
            return None

    @staticmethod
    def get_review_by_element_id(element_id):
        try:
            reviews = reviews_collection.find({"element_id": element_id}).sort("date", -1)
            return [ReviewModel.from_dict(r) for r in reviews]
        except Exception as e:
            print(f"Erreur get_by_element_id: {e}")
            return []

    @staticmethod
    def get_published_reviews():
        try:
            reviews = reviews_collection.find({"published": True}).sort("date", -1)
            return [ReviewModel.from_dict(r) for r in reviews]
        except Exception as e:
            print(f"Erreur get_published_reviews: {e}")
            return []

    @staticmethod
    def publish_review(review_id):
        try:
            result = reviews_collection.update_one(
                {"_id": ObjectId(review_id)},
                {"$set": {"published": True, "status": "published"}}
            )
            return result.modified_count > 0
        except Exception as e:
            print("Erreur publish_review:", e)
            return False

    @staticmethod
    def delete_review(review_id):
        """Supprime une review définitivement"""
        try:
            result = reviews_collection.delete_one({"_id": ObjectId(review_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Erreur delete_review: {e}")
            return False

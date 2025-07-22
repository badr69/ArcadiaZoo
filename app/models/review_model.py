from datetime import datetime
from app.db.mongo import reviews_collection

class Review:
    def __init__(self, pseudo, message, rating, element_id, date=None):
        self.pseudo = pseudo
        self.message = message
        self.rating = int(rating)
        self.element_id = element_id
        self.date = date or datetime.utcnow()

    def to_dict(self):
        return {
            "pseudo": self.pseudo,
            "message": self.message,
            "rating": self.rating,
            "element_id": self.element_id,
            "date": self.date
        }

    def save(self):
        reviews_collection.insert_one(self.to_dict())

    @staticmethod
    def from_dict(data):
        return Review(
            pseudo=data.get("pseudo"),
            message=data.get("message"),
            rating=data.get("rating"),
            element_id=data.get("element_id"),
            date=data.get("date")
        )

    @staticmethod
    def get_by_element_id(element_id):
        reviews = reviews_collection.find({"element_id": element_id})
        return [Review.from_dict(review) for review in reviews]

    @staticmethod
    def get_all():
        reviews = reviews_collection.find().sort("date", -1)
        reviews_list = [Review.from_dict(review) for review in reviews]
        print(f"Reviews récupérées: {len(reviews_list)}")  # debug
        return reviews_list







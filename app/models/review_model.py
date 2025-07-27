from datetime import datetime
from app.db.mongo import reviews_collection

class Review:
    def __init__(self, pseudo, message, rating, element_id, date=None, _id=None):
        self.pseudo = pseudo
        self.message = message
        self.rating = int(rating)
        self.element_id = element_id
        self.date = date or datetime.utcnow()
        self._id = str(_id) if _id else None

    def to_dict(self):
        data = {
            "pseudo": self.pseudo,
            "message": self.message,
            "rating": self.rating,
            "element_id": self.element_id,
            "date": self.date.isoformat() if self.date else None
        }
        if self._id:
            data["_id"] = self._id
        return data

    def save(self):
        result = reviews_collection.insert_one({
            "pseudo": self.pseudo,
            "message": self.message,
            "rating": self.rating,
            "element_id": self.element_id,
            "date": self.date
        })
        self._id = str(result.inserted_id)
        return self._id

    @staticmethod
    def from_dict(data):
        return Review(
            pseudo=data.get("pseudo"),
            message=data.get("message"),
            rating=data.get("rating"),
            element_id=data.get("element_id"),
            date=data.get("date"),
            _id=data.get("_id")
        )

    @staticmethod
    def get_all():
        try:
            reviews_cursor = reviews_collection.find().sort("date", -1)
            reviews_list = []
            for review_data in reviews_cursor:
                review_data["_id"] = str(review_data["_id"])
                # Convertir date Mongo (datetime) en iso string
                review_data["date"] = review_data["date"].isoformat() if review_data.get("date") else None
                reviews_list.append(review_data)
            return reviews_list
        except Exception as e:
            print("Erreur lors de la récupération des reviews :", e)
            return []

    @staticmethod
    def get_by_element_id(element_id):
        reviews_cursor = reviews_collection.find({"element_id": element_id}).sort("date", -1)
        reviews_list = []
        for review in reviews_cursor:
            review["_id"] = str(review["_id"])
            review["date"] = review["date"].isoformat() if review.get("date") else None
            reviews_list.append(review)
        return reviews_list





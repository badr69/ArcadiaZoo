from datetime import datetime, UTC
from app.db.mongo import db  # db est la base de données, pas le client

clicks_collection = db["animal_clicks"]  # collection dédiée aux clics

class AnimalClickModel:

    @staticmethod
    def get_clicks_by_animal(collection):
        """Retourne le nombre total de clics pour chaque animal"""
        pipeline = [
            {"$group": {
                "_id": "$animal_id",
                "total_clicks": {"$sum": 1}
            }},
            {"$sort": {"total_clicks": -1}}  # optionnel : trier par nombre de clics décroissant
        ]
        return list(collection.aggregate(pipeline))

    @staticmethod
    def add_click(collection, animal_id):
        """Enregistre un clic avec timestamp"""
        collection.insert_one({
            "animal_id": animal_id,
            "date": datetime.now(UTC)
        })

    @staticmethod
    def get_clicks_by_date(collection, animal_id):
        """Retourne le nombre de clics groupés par date"""
        pipeline = [
            {"$match": {"animal_id": animal_id}},
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]
        return list(collection.aggregate(pipeline))

    @staticmethod
    def get_clicks_for_animal_id(mongo_db, animal_id):
        collection = mongo_db["animal_clicks"]
        return collection.count_documents({"animal_id": animal_id})
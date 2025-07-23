from app.db.mongo import db

reviews_collection = db["reviews"]

for review in reviews_collection.find():
    print(review)

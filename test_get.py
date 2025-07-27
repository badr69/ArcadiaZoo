from app.models.review_model import Review
reviews = Review.get_all()
print(len(reviews))  # Doit afficher > 1 si plusieurs reviews existent
print([r.to_dict() for r in reviews])  # Vérifie la structure

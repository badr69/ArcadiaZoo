from app.models.review_model import ReviewModel

review = ReviewModel("Alice", "Très bon habitat", 5, "123")
review.save()

print("Avis sauvegardé avec succès !")

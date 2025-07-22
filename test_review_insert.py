from app.models.review_model import Review

review = Review("Alice", "Très bon habitat", 5, "123")
review.save()

print("Avis sauvegardé avec succès !")

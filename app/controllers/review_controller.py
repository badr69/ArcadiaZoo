from flask import request, jsonify
from app.models.review_model import ReviewModel

class ReviewController:

    @staticmethod
    def add_review():
        # TODO: Récupérer les données JSON envoyées par le client
        data = request.get_json()
        try:
            # TODO: Appeler le modèle pour ajouter une nouvelle review et récupérer son ID
            review_id = ReviewModel.add_review(data)
            # TODO: Retourner une réponse JSON avec succès et l'ID de la review créée
            return jsonify({"status": "success", "review_id": review_id}), 201
        except Exception as e:
            # TODO: Gérer les erreurs en renvoyant un message d'erreur JSON
            return jsonify({"status": "error", "message": str(e)}), 400

    @staticmethod
    def get_all_reviews():
        # TODO: Récupérer toutes les reviews depuis le modèle
        reviews = ReviewModel.get_all_reviews()
        # TODO: Convertir les reviews en dictionnaires pour JSON
        reviews_dict = [r.to_dict() for r in reviews]
        # TODO: Retourner les reviews au format JSON
        return jsonify(reviews_dict), 200

    @staticmethod
    def get_review_by_id(review_id):
        # TODO: Récupérer une review spécifique par son ID
        review = ReviewModel.get_review_by_id(review_id)
        if review:
            # TODO: Retourner la review au format JSON si trouvée
            return jsonify(review.to_dict()), 200
        else:
            # TODO: Retourner une erreur 404 si la review n’existe pas
            return jsonify({"status": "error", "message": "Review not found"}), 404

    @staticmethod
    def get_review_by_element_id(element_id):
        # TODO: Récupérer les reviews associées à un élément spécifique (par ex. produit ou service)
        reviews = ReviewModel.get_review_by_element_id(element_id)
        # TODO: Convertir les reviews en dictionnaires
        reviews_dict = [r.to_dict() for r in reviews]
        # TODO: Retourner les reviews au format JSON
        return jsonify(reviews_dict), 200

    @staticmethod
    def get_published_reviews():
        # TODO: Récupérer uniquement les reviews publiées
        reviews = ReviewModel.get_published_reviews()
        # TODO: Convertir en dictionnaires
        reviews_dict = [r.to_dict() for r in reviews]
        # TODO: Retourner la liste au format JSON
        return jsonify(reviews_dict), 200

    @staticmethod
    def publish_review(review_id):
        # TODO: Mettre à jour le statut d'une review pour la publier
        success = ReviewModel.publish_review(review_id)
        if success:
            # TODO: Confirmer la publication de la review
            return jsonify({"status": "success", "message": "Review published"}), 200
        else:
            # TODO: Retourner une erreur si la review est introuvable ou non modifiée
            return jsonify({"status": "error", "message": "Review not found or not updated"}), 404

    @staticmethod
    def delete_review(review_id):
        # TODO: Supprimer une review par son ID
        success = ReviewModel.delete_review(review_id)
        if success:
            # TODO: Confirmer la suppression
            return jsonify({"status": "success", "message": "Review deleted"}), 200
        else:
            # TODO: Retourner une erreur si la review n'existe pas
            return jsonify({"status": "error", "message": "Review not found"}), 404




# from flask import request, jsonify, abort
# from app.models.review_model import ReviewModel
#
# class ReviewController:
#
#     @staticmethod
#     def add_review():
#         data = request.get_json()
#         try:
#             review_id = ReviewModel.add_review(data)
#             return jsonify({"status": "success", "review_id": review_id}), 201
#         except Exception as e:
#             return jsonify({"status": "error", "message": str(e)}), 400
#
#     @staticmethod
#     def get_all_reviews():
#         reviews = ReviewModel.get_all_reviews()
#         reviews_dict = [r.to_dict() for r in reviews]
#         return jsonify(reviews_dict), 200
#
#     @staticmethod
#     def get_review_by_id(review_id):
#         review = ReviewModel.get_review_by_id(review_id)
#         if review:
#             return jsonify(review.to_dict()), 200
#         else:
#             return jsonify({"status": "error", "message": "Review not found"}), 404
#
#     @staticmethod
#     def get_review_by_element_id(element_id):
#         reviews = ReviewModel.get_review_by_element_id(element_id)
#         reviews_dict = [r.to_dict() for r in reviews]
#         return jsonify(reviews_dict), 200
#
#     @staticmethod
#     def get_published_reviews():
#         reviews = ReviewModel.get_published_reviews()
#         reviews_dict = [r.to_dict() for r in reviews]
#         return jsonify(reviews_dict), 200
#
#     @staticmethod
#     def publish_review(review_id):
#         success = ReviewModel.publish_review(review_id)
#         if success:
#             return jsonify({"status": "success", "message": "Review published"}), 200
#         else:
#             return jsonify({"status": "error", "message": "Review not found or not updated"}), 404
#
#     @staticmethod
#     def delete_review(review_id):
#         success = ReviewModel.delete_review(review_id)
#         if success:
#             return jsonify({"status": "success", "message": "Review deleted"}), 200
#         else:
#             return jsonify({"status": "error", "message": "Review not found"}), 404
#

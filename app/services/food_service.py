from app.models.food_model import FoodModel
from app.models.animal_model import AnimalModel

class FoodService:

    @staticmethod
    def list_all_foods():
        """Retourne tous les enregistrements de nourriture."""
        return FoodModel.list_all_foods()

    @staticmethod
    def get_food_by_id(food_id):
        """Retourne une nourriture spécifique par son ID."""
        return FoodModel.get_food_by_id(food_id)

    @staticmethod
    def create_food(food_model: FoodModel):
        """Crée une nouvelle entrée de nourriture."""
        try:
            food_id = food_model.create_food()
            if food_id:
                return {"status": True, "food_id": food_id}
            else:
                return {"status": False, "message": "Échec de la création de la nourriture."}
        except Exception as e:
            return {"status": False, "message": str(e)}

    @staticmethod
    def update_food(food_model: FoodModel):
        """Met à jour une nourriture existante."""
        try:
            success = food_model.update_food()  # sans argument
            if success:
                return {"status": True}
            else:
                return {"status": False, "message": "Échec de la mise à jour."}
        except Exception as e:
            return {"status": False, "message": str(e)}

    @staticmethod
    def delete_food(food_id):
        """Supprime une nourriture par ID."""
        try:
            success = FoodModel.delete_food(food_id)
            if success:
                return {"status": True}
            else:
                return {"status": False, "message": "Échec de la suppression."}
        except Exception as e:
            return {"status": False, "message": str(e)}

    @staticmethod
    def list_all_animals():
        """Retourne tous les animaux."""
        return AnimalModel.list_all_animals()

from app.models.animal_model import AnimalModel


class AnimalService:
    @staticmethod
    def create_animal(name, race, description, url_image):
        animal = AnimalModel.create_animal(name, race, description, url_image)
        if animal is None:
            return {"status": False, "message": "Erreur lors de la création de l'animal."}
        return {"status": True, "animal": animal}

    @staticmethod
    def list_all_animals():
        return AnimalModel.list_all_animals()

    @staticmethod
    def get_animal_by_id(animal_id):
        return AnimalModel.get_animal_by_id(animal_id)

    @staticmethod
    def update_animal(animal_id, name, description, race, url_image):
        success = AnimalModel.update_animal(animal_id, name, race, description, url_image)
        if not success:
            return {"status": False, "message": "Erreur lors de la mise à jour."}
        return {"status": True, "message": "animal mis à jour."}

    @staticmethod
    def delete_animal(animal_id):
        success =AnimalModel.delete_animal(animal_id)
        if not success:
            return {"status": False, "message": "Erreur lors de la suppression."}
        return {"status": True, "message": "animal supprimé."}

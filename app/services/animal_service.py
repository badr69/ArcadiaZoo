from app.models.animal_model import AnimalModel


class AnimalService:
    @staticmethod
    def create_animal(name, url_image, description):
        animal = AnimalModel.create_animal(name, url_image, description)
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
    def update_animal(animal_id, name, url_image, description):
        succes = AnimalModel.update_animal(animal_id, name, url_image, description)
        if not succes:
            return {"status": False, "message": "Erreur lors de la mise à jour."}
        return {"status": True, "message": "animal mis à jour."}

    @staticmethod
    def delete_animal(animal_id):
        succes =AnimalModel.delete_animal(animal_id)
        if not succes:
            return {"status": False, "message": "Erreur lors de la suppression."}
        return {"status": True, "message": "animal supprimé."}

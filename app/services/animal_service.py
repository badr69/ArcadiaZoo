from app.models.animal_model import AnimalModel

class AnimalService:

    @classmethod
    def create_animal(cls, name, race, description, url_image):
        if not name or not race:
            return {"status": False, "message": "Name and race are required."}

        animal = AnimalModel.create_animal(name, race, description, url_image)
        if not animal:
            return {"status": False, "message": "Erreur lors de la création de l'animal."}
        return {"status": True, "data": animal}

    @classmethod
    def list_all_animals(cls):
        animals = AnimalModel.list_all_animals()
        return {"status": True, "data": animals}

    @classmethod
    def get_animal_by_id(cls, animal_id):
        animal = AnimalModel.get_animal_by_id(animal_id)
        if not animal:
            return {"status": False, "message": "Animal non trouvé."}
        return {"status": True, "data": animal}

    @classmethod
    def update_animal(cls, animal_id, name, race, description, url_image):
        success = AnimalModel.update_animal(animal_id, name, race, description, url_image)
        if not success:
            return {"status": False, "message": f"Aucun animal trouvé avec l'id {animal_id}."}
        return {"status": True, "message": "Animal mis à jour avec succès."}

    @classmethod
    def delete_animal(cls, animal_id):
        success = AnimalModel.delete_animal(animal_id)
        if not success:
            return {"status": False, "message": f"Aucun animal trouvé avec l'id {animal_id}."}
        return {"status": True, "message": "Animal supprimé avec succès."}


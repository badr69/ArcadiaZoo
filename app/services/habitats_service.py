from app.models.habitats_model import Habitat


class HabitatService:
    @staticmethod
    def create_habitat(name, url_image, description):
        habitat = Habitat.create_habitat(name, url_image, description)
        if habitat is None:
            return {"status": False, "message": "Erreur lors de la création de l'habitat."}
        return {"status": True, "habitat": habitat}

    @staticmethod
    def list_all_habitats():
        return Habitat.list_all_habitats()

    @staticmethod
    def get_habitat_by_id(habitat_id):
        return Habitat.get_habitat_by_id(habitat_id)

    @staticmethod
    def update_habitat(habitat_id, name, url_image, description):
        success = Habitat.update_habitat(habitat_id, name, url_image, description)
        if not success:
            return {"status": False, "message": "Erreur lors de la mise à jour."}
        return {"status": True, "message": "Habitat mis à jour."}

    @staticmethod
    def delete_habitat(habitat_id):
        success = Habitat.delete_habitat(habitat_id)
        if not success:
            return {"status": False, "message": "Erreur lors de la suppression."}
        return {"status": True, "message": "Habitat supprimé."}

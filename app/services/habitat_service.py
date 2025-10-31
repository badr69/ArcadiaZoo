from app.models.habitat_model import Habitat

class HabitatService:
    @classmethod
    def create_habitat(cls, name, url_image, description):
        habitat = Habitat.create_habitat(name, url_image, description)
        if habitat is None:
            return {"status": False, "message": "Erreur lors de la création de l'habitat."}
        return {"status": True, "habitat": habitat}


    @classmethod
    def list_all_habitats(cls):
        return Habitat.list_all_habitats()

    @classmethod
    def get_habitat_by_id(cls, habitat_id):
        return Habitat.get_habitat_by_id(habitat_id)

    @classmethod
    def update_habitat(cls, habitat_id, name, url_image, description):
        success = Habitat.update_habitat(habitat_id, name, url_image, description)
        if not success:
            return {"status": False, "message": "Erreur lors de la mise à jour."}
        return {"status": True, "message": "Habitat mis à jour."}

    @classmethod
    def delete_habitat(cls, habitat_id):
        success = Habitat.delete_habitat(habitat_id)
        if not success:
            return {"status": False, "message": "Erreur lors de la suppression."}
        return {"status": True, "message": "Habitat supprimé."}





# from app.models.habitat_model import Habitat
#
#
# class HabitatService:
#     @staticmethod
#     def create_habitat(name, url_image, description):
#         habitat = Habitat.create_habitat(name, url_image, description)
#         if habitat is None:
#             return {"status": False, "message": "Erreur lors de la création de l'habitat."}
#         return {"status": True, "habitat": habitat}
#
#     @staticmethod
#     def list_all_habitats():
#         return Habitat.list_all_habitats()
#
#     @staticmethod
#     def get_habitat_by_id(habitat_id):
#         return Habitat.get_habitat_by_id(habitat_id)
#
#     @staticmethod
#     def update_habitat(habitat_id, name, url_image, description):
#         success = Habitat.update_habitat(habitat_id, name, url_image, description)
#         if not success:
#             return {"status": False, "message": "Erreur lors de la mise à jour."}
#         return {"status": True, "message": "Habitat mis à jour."}
#
#     @staticmethod
#     def delete_habitat(habitat_id):
#         success = Habitat.delete_habitat(habitat_id)
#         if not success:
#             return {"status": False, "message": "Erreur lors de la suppression."}
#         return {"status": True, "message": "Habitat supprimé."}

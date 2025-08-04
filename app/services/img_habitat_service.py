from app.models.img_habitat_model import ImgHabitat

class ImgHabitatService:
    @staticmethod
    def get_all():
        return ImgHabitat.get_all()

    @staticmethod
    def get_by_id(image_id):
        img = ImgHabitat.get_by_id(image_id)
        if img is None:
            raise LookupError(f"Image avec id {image_id} non trouvée")
        return img

    @staticmethod
    def create(habitat_id, filename, description=None):
        if not habitat_id or not filename:
            raise ValueError("habitat_id et filename sont requis")
        new_id = ImgHabitat.create(habitat_id, filename, description)
        return new_id

    @staticmethod
    def update(image_id, habitat_id, filename, description=None):
        if not habitat_id or not filename:
            raise ValueError("habitat_id et filename sont requis")

        img = ImgHabitat.get_by_id(image_id)
        if img is None:
            raise LookupError(f"Image avec id {image_id} non trouvée")

        ImgHabitat.update(image_id, habitat_id, filename, description)

    @staticmethod
    def delete(image_id):
        img = ImgHabitat.get_by_id(image_id)
        if img is None:
            raise LookupError(f"Image avec id {image_id} non trouvée")

        ImgHabitat.delete(image_id)

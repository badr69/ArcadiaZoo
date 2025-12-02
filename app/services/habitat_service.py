from app.models.habitat_model import HabitatModel
from app.utils.security import sanitize_html, detect_sql_injection

class HabitatService:
    """
    Service pour gérer la logique métier des habitats.
    """

    @classmethod
    def list_all_habitats(cls):
        return HabitatModel.list_all_habitats()

    @classmethod
    def get_habitat_by_id(cls, habitat_id):
        habitat = HabitatModel.get_habitat_by_id(habitat_id)
        if not habitat:
            return None, "Habitat introuvable."
        return habitat, None

    @classmethod
    def create_habitat(cls, name, url_image, description):
        # ------------------------
        # LOGIQUE MÉTIER
        # ------------------------
        name = sanitize_html(name)
        description = sanitize_html(description)

        if detect_sql_injection(name) or detect_sql_injection(description):
            return None, "Entrée invalide détectée."

        if not name or len(name) < 3:
            return None, "Le nom doit contenir au moins 3 caractères."

        habitat = HabitatModel.create_habitat(name, url_image, description)
        if not habitat:
            return None, "Nom déjà utilisé ou erreur lors de la création."
        return habitat, None

    def __init__(self, habitat_id):
        self.habitat = HabitatModel.get_habitat_by_id(habitat_id)

    def exists(self):
        return self.habitat is not None

    def update_habitat(self, name, url_image, description):
        if not self.exists():
            return False, "Habitat introuvable."

        # ------------------------
        # LOGIQUE MÉTIER
        # ------------------------
        name = sanitize_html(name)
        description = sanitize_html(description)

        if detect_sql_injection(name) or detect_sql_injection(description):
            return False, "Entrée invalide détectée."

        if not name or len(name) < 3:
            return False, "Le nom doit contenir au moins 3 caractères."

        success = self.habitat.update_habitat(name, url_image, description)
        if not success:
            return False, "Nom déjà utilisé ou erreur lors de la mise à jour."
        return True, None

    def delete_habitat(self):
        if not self.exists():
            return False, "Habitat introuvable."
        success = self.habitat.delete_habitat()
        if not success:
            return False, "Erreur lors de la suppression."
        return True, None



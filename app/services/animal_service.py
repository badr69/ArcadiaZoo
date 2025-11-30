import unicodedata
from app.models.animal_model import AnimalModel
from app.utils.security import sanitize_html, detect_sql_injection

def normalize_text(text):
    return unicodedata.normalize("NFKD", text)

class AnimalService:

    @classmethod
    def list_all_animals(cls):
        return AnimalModel.list_all_animals()

    @classmethod
    def get_animal_by_id(cls, animal_id):
        animal = AnimalModel.get_animal_by_id(animal_id)
        if not animal:
            return None, "Animal introuvable."
        return animal, None

    @classmethod
    def create_animal(cls, name, race, description, url_image, habitat_id):
        # name = sanitize_html(name)
        # race = sanitize_html(race)
        # description = sanitize_html(description)
        name = sanitize_html(normalize_text(name))
        race = sanitize_html(normalize_text(race))
        description = sanitize_html(normalize_text(description))
        # récupère le fichier uploadé (ici la ligne manquante)

        print("DEBUG create_animal:", name, race, description, habitat_id)

        if detect_sql_injection(name) or detect_sql_injection(race) or detect_sql_injection(description):
            return None, "Entrée invalide détectée."

        if not name or len(name) < 3:
            return None, "Le nom doit contenir au moins 3 caractères."
        if not race or len(race) < 2:
            return None, "La race doit contenir au moins 2 caractères."

        animal = AnimalModel.create_animal(name, race, description, url_image, habitat_id)
        if not animal:
            return None, "Erreur lors de la création ou nom déjà utilisé."
        return animal, None

    def __init__(self, animal_id):
        self.animal = AnimalModel.get_animal_by_id(animal_id)

    def exists(self):
        return self.animal is not None

    def update_animal(self, name, race, description, url_image, habitat_id):
        if not self.exists():
            return False, "Animal introuvable."

        # name = sanitize_html(name)
        # race = sanitize_html(race)
        # description = sanitize_html(description)
        name = sanitize_html(normalize_text(name))
        race = sanitize_html(normalize_text(race))
        description = sanitize_html(normalize_text(description))

        if detect_sql_injection(name) or detect_sql_injection(race) or detect_sql_injection(description):
            return False, "Entrée invalide détectée."

        success = self.animal.update_animal(name, race, description, url_image, habitat_id)
        if not success:
            return False, "Erreur lors de la mise à jour."
        return True, None

    def delete_animal(self):
        if not self.exists():
            return False, "Animal introuvable."
        success = self.animal.delete_animal()
        if not success:
            return False, "Erreur lors de la suppression."
        return True, None

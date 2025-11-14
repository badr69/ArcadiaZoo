from app.models.habitat_model import HabitatModel

class HabitatService:

    @classmethod
    def list_all_habitats(cls):
        """Récupère tous les habitats"""
        habitats = HabitatModel.list_all_habitats()
        # TODO : appliquer un filtre si nécessaire (ex : habitats actifs)
        return habitats

    @classmethod
    def get_habitat_by_id(cls, habitat_id):
        """Récupère un habitat par son id"""
        habitat = HabitatModel.get_habitat_by_id(habitat_id)
        if not habitat:
            # TODO : gérer l'erreur si habitat inexistant
            print(f"Habitat avec id {habitat_id} introuvable")
        return habitat

    @classmethod
    def create_habitat(cls, name, description, url_image):
        """Création d'un nouvel habitat"""
        # Vérification que le nom n'existe pas déjà
        existing = [h for h in HabitatModel.list_all_habitats() if h.name == name]
        if existing:
            # TODO : retourner un message d'erreur plus structuré
            print(f"Un habitat avec le nom '{name}' existe déjà")
            return None

        # TODO : vérifier que url_image est valide ou respecter certaines règles
        habitat = HabitatModel.create_habitat(name, description, url_image)
        return habitat

    @classmethod
    def update_habitat(cls, habitat_id, name, description, url_image):
        """Met à jour un habitat existant"""
        habitat = HabitatModel.get_habitat_by_id(habitat_id)
        if not habitat:
            # TODO : retourner une exception ou message d'erreur
            print(f"Aucun habitat trouvé avec l'id {habitat_id}")
            return False

        # TODO : vérifier que le nouveau nom n'est pas déjà utilisé par un autre habitat
        all_habitats = HabitatModel.list_all_habitats()
        if any(h.name == name and h.habitat_id != habitat_id for h in all_habitats):
            print(f"Le nom '{name}' est déjà utilisé par un autre habitat")
            return False

        return HabitatModel.update_habitat(habitat_id, name, description, url_image)

    @classmethod
    def delete_habitat(cls, habitat_id):
        """Supprime un habitat"""
        habitat = HabitatModel.get_habitat_by_id(habitat_id)
        if not habitat:
            # TODO : gérer le cas où l'habitat n'existe pas
            print(f"Aucun habitat trouvé avec l'id {habitat_id} à supprimer")
            return False

        # TODO : vérifier si des animaux ou images dépendent de cet habitat avant suppression
        return HabitatModel.delete_habitat(habitat_id)

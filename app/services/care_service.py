from app.models.care_model import CareModel
from datetime import datetime, date


class CareService:

    @classmethod
    def list_all_cares(cls):
        """Retourne la liste complète des soins."""
        try:
            return CareModel.list_all_cares()
        except Exception as e:
            print(f"[CareService.list_all_cares] Erreur: {e}")
            return []

    @classmethod
    def get_care_by_id(cls, care_id):
        """Récupère un soin par son identifiant."""
        try:
            care = CareModel.get_care_by_id(care_id)
            if not care:
                print(f"[CareService.get_care_by_id] Aucun soin trouvé avec id {care_id}")
                return None
            return care
        except Exception as e:
            print(f"[CareService.get_care_by_id] Erreur: {e}")
            return None

    @staticmethod
    def create_care(animal_id, user_id, type_care, description, date_care=None):
        """Crée un nouveau rapport de soin."""
        try:
            # Validation basique
            if not animal_id:
                raise ValueError("L'ID de l'animal est requis.")
            if not user_id:
                raise ValueError("L'ID du vétérinaire est requis.")
            if not type_care:
                raise ValueError("Le type de soin est requis.")

            # ✅ Conversion auto en datetime si nécessaire
            if isinstance(date_care, date) and not isinstance(date_care, datetime):
                date_care = datetime(date_care.year, date_care.month, date_care.day)
            elif date_care is None:
                date_care = datetime.now()

            if not isinstance(date_care, datetime):
                raise ValueError("date_care doit être un objet datetime valide.")

            # Appel du modèle
            care = CareModel.create_care(animal_id, user_id, type_care, description, date_care)
            if not care:
                print("[CareService.create_care] Erreur: impossible de créer le soin.")
                return None

            return care

        except Exception as e:
            print(f"[CareService.create_care] Erreur: {e}")
            return None

    @staticmethod
    def update_care(care_id, animal_id, user_id, type_care, description, date_care=None):
        """Met à jour un rapport de soin existant."""
        try:
            if not care_id:
                raise ValueError("L'ID du soin est requis.")
            if not animal_id:
                raise ValueError("L'ID de l'animal est requis.")
            if not user_id:
                raise ValueError("L'ID du vétérinaire est requis.")
            if not type_care:
                raise ValueError("Le type de soin est requis.")

            # ✅ Conversion auto en datetime si nécessaire
            if isinstance(date_care, date) and not isinstance(date_care, datetime):
                date_care = datetime(date_care.year, date_care.month, date_care.day)
            elif date_care is None:
                date_care = datetime.now()

            if not isinstance(date_care, datetime):
                raise ValueError("date_care doit être un objet datetime valide.")

            success = CareModel.update_care(care_id, animal_id, user_id, type_care, description, date_care)
            if not success:
                print(f"[CareService.update_care] Impossible de mettre à jour le soin avec id {care_id}")
                return False

            return True

        except Exception as e:
            print(f"[CareService.update_care] Erreur: {e}")
            return False

    @staticmethod
    def delete_care(care_id):
        """Supprime un rapport de soin par son ID."""
        try:
            if not care_id:
                raise ValueError("L'ID du soin est requis.")

            success = CareModel.delete_care(care_id)
            if not success:
                print(f"[CareService.delete_care] Impossible de supprimer le soin avec id {care_id}")
                return False
            return True

        except Exception as e:
            print(f"[CareService.delete_care] Erreur: {e}")
            return False


# app/services/care_service.py
from app.models.care_model import CareModel
from app import UserModel
from app.utils.security import sanitize_html, detect_sql_injection

class CareService:
    """
    Service OOP pour gérer la logique métier des soins (Care).
    """

    # ======================================================
    # LIST ALL CARES
    # ======================================================
    @classmethod
    def list_all_cares(cls):
        try:
            cares = CareModel.list_all_cares()
            return cares, None
        except Exception as e:
            print(f"[CareService.list_all_cares error]: {e}")
            return [], "Erreur lors de la récupération des soins."

    # ======================================================
    # LIST ALL VETS
    # ======================================================
    @classmethod
    def list_all_vets(cls):
        try:
            vets = UserModel.list_all_vets()
            if not vets:
                return [], "Aucun vétérinaire trouvé."
            return vets, None
        except Exception as e:
            print(f"[CareService.list_all_vets error]: {e}")
            return [], "Erreur lors de la récupération des vétérinaires."

    # ======================================================
    # GET CARE BY ID
    # ======================================================
    @classmethod
    def get_care_by_id(cls, care_id):
        try:
            care = CareModel.get_care_by_id(care_id)
            if not care:
                return None, "Soin introuvable."
            return care, None
        except Exception as e:
            print(f"[CareService.get_care_by_id error]: {e}")
            return None, "Erreur lors de la récupération du soin."

    # ======================================================
    # CREATE CARE
    # ======================================================
    @classmethod
    def create_care(cls, animal_id, user_id, type_care, description, date_care=None):
        try:
            type_care = sanitize_html(type_care)
            description = sanitize_html(description)

            if detect_sql_injection(type_care) or detect_sql_injection(description):
                return None, "Entrée invalide détectée."

            if len(type_care) < 3:
                return None, "Le type de soin doit contenir au moins 3 caractères."

            care = CareModel.create_care(animal_id, user_id, type_care, description, date_care)
            if not care:
                return None, "Erreur lors de la création du soin."

            return care, None

        except Exception as e:
            print(f"[CareService.create_care error]: {e}")
            return None, "Erreur lors de la création du soin."

    # ======================================================
    # INSTANCE (POUR UPDATE & DELETE)
    # ======================================================
    def __init__(self, care_id):
        try:
            self.care = CareModel.get_care_by_id(care_id)
        except Exception as e:
            print(f"[CareService.__init__ error]: {e}")
            self.care = None

    def exists(self):
        return self.care is not None

    # ======================================================
    # UPDATE CARE (OOP)
    # ======================================================
    def update_care(self, animal_id, user_id, type_care, description, date_care=None):
        if not self.exists():
            return False, "Soin introuvable."
        try:
            type_care = sanitize_html(type_care)
            description = sanitize_html(description)
            if len(type_care) < 3:
                return False, "Le type de soin doit contenir au moins 3 caractères."

            success = self.care.update_care(
                animal_id=animal_id,
                user_id=user_id,
                type_care=type_care,
                description=description,
                date_care=date_care
            )
            if not success:
                return False, "Erreur lors de la mise à jour du soin."
            return True, None
        except Exception as e:
            print(f"[CareService.update_care error]: {e}")
            return False, "Erreur lors de la mise à jour du soin."

    # ======================================================
    # DELETE CARE (OOP)
    # ======================================================
    def delete_care(self):
        if not self.exists():
            return False, "Soin introuvable."

        try:
            success = self.care.delete_care()
            if not success:
                return False, "Erreur lors de la suppression."
            return True, None

        except Exception as e:
            print(f"[CareService.delete_care error]: {e}")
            return False, "Erreur lors de la suppression."

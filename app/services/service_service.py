from app.models.service_model import ServiceModel
from app.utils.security import sanitize_html, detect_sql_injection

class ServiceService:
    """
    Service pour gérer la logique métier des services.
    """


    @classmethod
    def list_all_services(cls):
        return ServiceModel.list_all_services()

    @classmethod
    def get_service_by_id(cls, service_id):
        service = ServiceModel.get_service_by_id(service_id)
        if not service:
            return None, "Service introuvable."
        return service, None

    @classmethod
    def create_service(cls, name, description, url_image):
        # ------------------------
        # LOGIQUE MÉTIER
        # ------------------------
        name = sanitize_html(name)
        description = sanitize_html(description)

        if detect_sql_injection(name) or detect_sql_injection(description):
            return None, "Entrée invalide détectée."

        if not name or len(name) < 3:
            return None, "Le nom doit contenir au moins 3 caractères."

        service = ServiceModel.create_service(name, description, url_image)
        if not service:
            return None, "Nom déjà utilisé ou erreur lors de la création."
        return service, None

    def __init__(self, service_id):
        self.service = ServiceModel.get_service_by_id(service_id)

    def exists(self):
        return self.service is not None

    def update_service(self, name, description, url_image):
        if not self.exists():
            return False, "Service introuvable."

        # ------------------------
        # LOGIQUE MÉTIER
        # ------------------------
        name = sanitize_html(name)
        description = sanitize_html(description)

        if detect_sql_injection(name) or detect_sql_injection(description):
            return False, "Entrée invalide détectée."

        if not name or len(name) < 3:
            return False, "Le nom doit contenir au moins 3 caractères."

        success = self.service.update_service(name, description, url_image)
        if not success:
            return False, "Nom déjà utilisé ou erreur lors de la mise à jour."
        return True, None

    def delete_service(self):
        if not self.exists():
            return False, "Service introuvable."
        success = self.service.delete_service()
        if not success:
            return False, "Erreur lors de la suppression."
        return True, None


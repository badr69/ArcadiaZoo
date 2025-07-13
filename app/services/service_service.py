from app.models.service_model import ServiceModel


class ServiceService:
    @staticmethod
    def create_service(name, url_image, description):
        service = ServiceModel.create_service(name, url_image, description)
        if service is None:
            return {"status": False, "message": "Erreur lors de la création de l'service."}
        return {"status": True, "service": service}

    @staticmethod
    def list_all_services():
        return ServiceModel.list_all_services()

    @staticmethod
    def get_service_by_id(service_id):
        return ServiceModel.get_service_by_id(service_id)

    @staticmethod
    def update_service(service_id, name, url_image, description):
        succes = ServiceModel.update_service(service_id, name, url_image, description)
        if not succes:
            return {"status": False, "message": "Erreur lors de la mise à jour."}
        return {"status": True, "message": "service mis à jour."}

    @staticmethod
    def delete_service(service_id):
        succes =ServiceModel.delete_service(service_id)
        if not succes:
            return {"status": False, "message": "Erreur lors de la suppression."}
        return {"status": True, "message": "service supprimé."}

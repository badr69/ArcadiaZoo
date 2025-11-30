from app.models.service_model import ServiceModel


class ServiceService:
    @classmethod
    def create_service(cls, name, url_image, description):
        try:
            service = ServiceModel.create_service(name, url_image, description)
            if service is None:
                return {"status": False, "message": "Erreur lors de la création du service."}
            return {"status": True, "service": service}
        except Exception as e:
            print(f"[ServiceService.create_service error]: {e}")
            return {"status": False, "message": "Erreur interne lors de la création du service."}

    @classmethod
    def list_all_services(cls):
        try:
            services = ServiceModel.list_all_services()
            return {"status": True, "services": services}
        except Exception as e:
            print(f"[ServiceService.list_all_services error]: {e}")
            return {"status": False, "message": "Erreur interne lors du chargement des services."}

    @classmethod
    def get_service_by_id(cls, service_id):
        try:
            service = ServiceModel.get_service_by_id(service_id)
            if service:
                return {"status": True, "service": service}
            return {"status": False, "message": "Service introuvable."}
        except Exception as e:
            print(f"[ServiceService.get_service_by_id error]: {e}")
            return {"status": False, "message": "Erreur interne lors de la récupération du service."}

    @classmethod
    def update_service(cls, service_id, name, url_image, description):
        try:
            success = ServiceModel.update_service(service_id, name, url_image, description)
            if not success:
                return {"status": False, "message": "Erreur lors de la mise à jour du service."}
            return {"status": True, "message": "Service mis à jour avec succès."}
        except Exception as e:
            print(f"[ServiceService.update_service error]: {e}")
            return {"status": False, "message": "Erreur interne lors de la mise à jour."}

    @classmethod
    def delete_service(cls, service_id):
        try:
            success = ServiceModel.delete_service(service_id)
            if not success:
                return {"status": False, "message": "Erreur lors de la suppression du service."}
            return {"status": True, "message": "Service supprimé avec succès."}
        except Exception as e:
            print(f"[ServiceService.delete_service error]: {e}")
            return {"status": False, "message": "Erreur interne lors de la suppression."}






import os
from pathlib import Path
from app.forms import ServiceCreateForm, ServiceUpdateForm
from app.services.service_service import ServiceService
from flask import render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app
from werkzeug.datastructures import FileStorage



class ServiceController:
    @staticmethod
    def list_all_services():
        services = ServiceService.list_all_services()
        return render_template('service/list_all_services.html', services=services)

    @staticmethod
    def get_service_by_id(service_id):
        service = ServiceService.get_service_by_id(service_id)
        if service is None:
            flash("service non trouvé.", "danger")
            return redirect(url_for('service.list_services'))
        return render_template('service/service_details.html', service=service)



    @staticmethod
    def create_service():
        form = ServiceCreateForm()

        # Debug éventuel (à supprimer en production)
        current_app.logger.debug("Form errors: %s", form.errors)

        if form.validate_on_submit():
            name = form.name.data
            description = form.description.data
            file = form.url_image.data  # FileStorage ou None

            # 1) Vérifier qu’un fichier a bien été téléversé
            if not file or file.filename == "":
                flash("Veuillez ajouter une image.", "danger")
                return render_template("service/create_service.html", form=form)

            # 2) Sauvegarder l’image
            try:
                filename = secure_filename(file.filename)
                upload_dir = Path(current_app.root_path) / "static" / "uploads"
                upload_dir.mkdir(parents=True, exist_ok=True)

                filepath = upload_dir / filename
                file.save(filepath)

                # Chemin à enregistrer en BDD
                url_image = f"/static/uploads/{filename}"

                # 3) Appeler le service
                result = ServiceService.create_service(
                    name=name,
                    url_image=url_image,
                    description=description
                )

                if result.get("status"):
                    flash("service créé avec succès.", "success")
                    return redirect(url_for("service.list_all_services"))

                flash(result.get("message", "Erreur inconnue lors de la création."), "danger")

            except Exception:
                current_app.logger.exception("Erreur lors de la création de l'service")
                flash("Une erreur est survenue pendant la création de l’service.", "danger")

        # GET initial ou formulaire invalide
        return render_template("service/create_service.html", form=form)



    @staticmethod
    def update_service(service_id):
        service = ServiceService.get_service_by_id(service_id)
        if service is None:
            flash("service non trouvé.", "danger")
            return redirect(url_for('service.list_all_services'))

        form = ServiceUpdateForm(obj=service)

        if form.validate_on_submit():
            name = form.name.data
            description = form.description.data
            file = form.url_image.data

            if isinstance(file, FileStorage) and file.filename:  # vérifie si un fichier est uploadé
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                file.save(upload_path)
                url_image = f'/static/uploads/{filename}'
            else:
                url_image = service.url_image  # garder l'image existante

            result = ServiceService.update_service(service_id, name, description, url_image)
            if result['status']:
                flash("service mis à jour.", "success")
                return redirect(url_for('service.list_all_services'))
            else:
                flash(result['message'], "danger")

        return render_template('service/update_service.html', form=form, service=service)

    @staticmethod
    def delete_service(service_id):
        result = ServiceService.delete_service(service_id)
        if result['status']:
            flash("service supprimé.", "success")
        else:
            flash(result['message'], "danger")
        return redirect(url_for('service.list_all_services'))

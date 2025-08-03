import os
from pathlib import Path
from app.forms.service_forms import ServiceCreateForm, ServiceUpdateForm
from app.services.service_service import ServiceService
from flask import render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app
from werkzeug.datastructures import FileStorage
from app.utils.security import detect_sql_injection, sanitize_html


class ServiceController:
    @staticmethod
    def list_all_services():
        # TODO: Récupérer tous les services via le service métier
        services = ServiceService.list_all_services()
        # TODO: Afficher la liste des services dans le template dédié
        return render_template('service/list_all_services.html', services=services)

    @staticmethod
    def get_service_by_id(service_id):
        # TODO: Récupérer le service avec l'ID donné
        service = ServiceService.get_service_by_id(service_id)
        if service is None:
            # TODO: Si service introuvable, afficher message d'erreur et rediriger vers liste des services
            flash("service not found.", "danger")
            return redirect(url_for('service.list_all_services'))  # correction de la route
        # TODO: Sinon afficher la page de détails du service
        return render_template('service/service_details.html', service=service)


    @staticmethod
    def create_service():
        form = ServiceCreateForm()

        # TODO: Valider le formulaire à la soumission
        if form.validate_on_submit():
            # TODO: Nettoyer les inputs pour éviter XSS
            name = sanitize_html(form.name.data)
            description = sanitize_html(form.description.data)

            # TODO: Détecter tentative d'injection SQL
            if detect_sql_injection(name) or detect_sql_injection(description):
                flash("Invalide Input.", "danger")
                return render_template("service/create_service.html", form=form)

            file = form.url_image.data  # FileStorage ou None

            # TODO: Vérifier qu’un fichier image a bien été téléversé
            if not file or file.filename == "":
                flash("Please add an image.", "danger")
                return render_template("service/create_service.html", form=form)

            # TODO: Sauvegarder l’image dans le dossier configuré
            try:
                filename = secure_filename(file.filename)
                upload_dir = Path(current_app.config['SERVICE_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)

                filepath = upload_dir / filename
                file.save(filepath)

                # TODO: Préparer le chemin à enregistrer en base
                url_image = f"uploads/service_img/{filename}"

                # TODO: Appeler le service métier pour créer le service
                result = ServiceService.create_service(
                    name=name,
                    url_image=url_image,
                    description=description
                )
                if result.get("status"):
                    flash("service created with success.", "success")
                    return redirect(url_for("service.list_all_services"))

                flash(result.get("message", "Unknown Error when creation."), "danger")

            except Exception:
                # TODO: Logger l’erreur et afficher un message utilisateur
                current_app.logger.exception("Erreur lors de la création de l'service")
                flash("Une erreur est survenue pendant la création de l’service.", "danger")
        # TODO: Afficher le formulaire (avec erreurs éventuelles)
        return render_template("service/create_service.html", form=form)

    @staticmethod
    def update_service(service_id):
        # TODO: Récupérer le service à modifier
        service = ServiceService.get_service_by_id(service_id)
        if service is None:
            flash("service not found.", "danger")
            return redirect(url_for('service.list_all_services'))

        form = ServiceUpdateForm(obj=service)

        # TODO: Valider le formulaire à la soumission
        if form.validate_on_submit():
            # TODO: Nettoyer les champs pour éviter XSS
            name = sanitize_html(form.name.data)
            description = sanitize_html(form.description.data)

            # TODO: Détecter tentative d'injection SQL
            if detect_sql_injection(name) or detect_sql_injection(description):
                flash("Invalide Input.", "danger")
                return render_template("service/create_service.html", form=form)

            file = form.url_image.data

            # TODO: Si un nouveau fichier a été uploadé, sauvegarder et mettre à jour le chemin
            if isinstance(file, FileStorage) and file.filename:
                filename = secure_filename(file.filename)
                upload_dir = Path(current_app.config['SERVICE_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)

                filepath = upload_dir / filename
                file.save(filepath)
                url_image = f'uploads/service_img/{filename}'  # Correction du chemin ici
            else:
                # TODO: Sinon garder l’image existante
                url_image = service.url_image

            # TODO: Appeler le service métier pour mettre à jour le service
            result = ServiceService.update_service(service_id, name, url_image, description)  # Correction de l’ordre des arguments
            if result['status']:
                flash("service updated.", "success")
                return redirect(url_for('service.list_all_services'))
            else:
                flash(result['message'], "danger")

        # TODO: Afficher le formulaire de mise à jour avec données existantes
        return render_template('service/update_service.html', form=form, service=service)

    @staticmethod
    def delete_service(service_id):
        # TODO: Appeler le service métier pour supprimer le service
        result = ServiceService.delete_service(service_id)
        if result['status']:
            flash("service deleted.", "success")
        else:
            flash(result['message'], "danger")
        # TODO: Rediriger vers la liste des services
        return redirect(url_for('service.list_all_services'))




# import os
# from pathlib import Path
# from app.forms.service_forms import ServiceCreateForm, ServiceUpdateForm
# from app.services.service_service import ServiceService
# from flask import render_template, redirect, url_for, flash
# from werkzeug.utils import secure_filename
# from flask import current_app
# from werkzeug.datastructures import FileStorage
# from app.utils.security import detect_sql_injection, sanitize_html
#
#
# class ServiceController:
#     @staticmethod
#     def list_all_services():
#         services = ServiceService.list_all_services()
#         return render_template('service/list_all_services.html', services=services)
#
#     @staticmethod
#     def get_service_by_id(service_id):
#         service = ServiceService.get_service_by_id(service_id)
#         if service is None:
#             flash("service not found.", "danger")
#             return redirect(url_for('service.list_all_services'))
#         return render_template('service/service_details.html', service=service)
#
#
#     @staticmethod
#     def create_service():
#         form = ServiceCreateForm()
#
#         # # Debug éventuel (à supprimer en production)
#         # current_app.logger.debug("Form errors: %s", form.errors)
#
#         if form.validate_on_submit():
#             name = sanitize_html(form.name.data)
#             description = sanitize_html(form.description.data)
#
#             if detect_sql_injection(name) or detect_sql_injection(description):
#                 flash("Invalide Input.", "danger")
#                 return render_template("service/create_service.html", form=form)
#
#             file = form.url_image.data  # FileStorage ou None
#
#             # 1) Vérifier qu’un fichier a bien été téléversé
#             if not file or file.filename == "":
#                 flash("Please add an image.", "danger")
#                 return render_template("service/create_service.html", form=form)
#
#             # 1) Sauvegarder l’image
#             try:
#                 filename = secure_filename(file.filename)
#                 upload_dir = Path(current_app.config['SERVICE_IMG_FOLDER'])
#                 upload_dir.mkdir(parents=True, exist_ok=True)
#
#                 filepath = upload_dir / filename
#                 file.save(filepath)
#
#                 # 2) Chemin à enregistrer en BDD
#                 url_image = f"uploads/service_img/{filename}"
#
#                 # 3)Appeler le service
#                 result = ServiceService.create_service(
#                     name=name,
#                     url_image=url_image,
#                     description=description
#                 )
#                 if result.get("status"):
#                     flash("service created with success.", "success")
#                     return redirect(url_for("service.list_all_services"))
#
#                 flash(result.get("message", "Unknown Error when creation."), "danger")
#
#             except Exception:
#                 current_app.logger.exception("Erreur lors de la création de l'service")
#                 flash("Une erreur est survenue pendant la création de l’service.", "danger")
#         return render_template("service/create_service.html", form=form)
#
#     @staticmethod
#     def update_service(service_id):
#         service = ServiceService.get_service_by_id(service_id)
#         if service is None:
#             flash("service not found.", "danger")
#             return redirect(url_for('service.list_all_services'))
#
#         form = ServiceUpdateForm(obj=service)
#
#         if form.validate_on_submit():
#             name = sanitize_html(form.name.data)
#             description = sanitize_html(form.description.data)
#
#             if detect_sql_injection(name) or detect_sql_injection(description):
#                 flash("Invalide Input.", "danger")
#                 return render_template("service/create_service.html", form=form)
#
#             file = form.url_image.data
#
#             if isinstance(file, FileStorage) and file.filename:  # vérifie si un fichier est uploadé
#                 filename = secure_filename(file.filename)
#                 upload_dir = Path(current_app.config['SERVICE_IMG_FOLDER'])
#                 upload_dir.mkdir(parents=True, exist_ok=True)
#
#                 filepath = upload_dir / filename
#                 file.save(filepath)
#                 url_image = f'uploads/service.img/{filename}'
#             else:
#                 url_image = service.url_image  # garder l'image existante
#
#             result = ServiceService.update_service(service_id, name, description, url_image)
#             if result['status']:
#                 flash("service updated.", "success")
#                 return redirect(url_for('service.list_all_services'))
#             else:
#                 flash(result['message'], "danger")
#
#         return render_template('service/update_service.html', form=form, service=service)
#
#     @staticmethod
#     def delete_service(service_id):
#         result = ServiceService.delete_service(service_id)
#         if result['status']:
#             flash("service deleted.", "success")
#         else:
#             flash(result['message'], "danger")
#         return redirect(url_for('service.list_all_services'))

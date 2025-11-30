from pathlib import Path
from flask import render_template, redirect, url_for, flash, current_app
from psycopg2 import DatabaseError, OperationalError
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from app.forms.service_forms import ServiceCreateForm, ServiceUpdateForm
from app.services.service_service import ServiceService
from app.utils.security import detect_sql_injection, sanitize_html


class ServiceController:

    @staticmethod
    def list_all_services():
        result = ServiceService.list_all_services()
        if not result.get("status"):
            flash(result.get("message", "Erreur lors du chargement des services."), "danger")
            services = []
        else:
            services = result.get("services", [])
        return render_template('service/list_all_services.html', services=services)

    @staticmethod
    def get_service_by_id(service_id):
        result = ServiceService.get_service_by_id(service_id)
        if not result.get("status"):
            flash(result.get("message", "Service introuvable."), "danger")
            return redirect(url_for('service.list_all_services'))
        service = result.get("service")
        return render_template('service/service_details.html', service=service)



    @staticmethod
    def create_service():
        form = ServiceCreateForm()

        if form.validate_on_submit():
            name = sanitize_html(form.name.data)
            description = sanitize_html(form.description.data)

            # Vérification basique contre l'injection
            if detect_sql_injection(name) or detect_sql_injection(description):
                flash("Entrée invalide détectée.", "danger")
                return render_template("service/create_service.html", form=form)

            file = form.url_image.data

            if not file or file.filename.strip() == "":
                flash("Veuillez ajouter une image.", "danger")
                return render_template("service/create_service.html", form=form)

            try:
                # Sauvegarde de l’image
                filename = secure_filename(file.filename)
                upload_dir = Path(current_app.config['SERVICE_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)

                filepath = upload_dir / filename
                file.save(filepath)

                # Construction du chemin relatif pour la base
                url_image = f"uploads/service_img/{filename}"

                # Appel au service métier
                result = ServiceService.create_service(name, url_image, description)

                if result.get("status"):
                    flash("Service créé avec succès.", "success")
                    return redirect(url_for("service.list_all_services"))

                flash(result.get("message", "Erreur inconnue lors de la création."), "danger")

            # --- Exceptions spécifiques d'abord ---
            except (DatabaseError, OperationalError) as db_err:
                current_app.logger.error(f"Erreur base de données : {db_err}")
                flash("Erreur de base de données lors de la création du service.", "danger")

            except FileNotFoundError as file_err:
                current_app.logger.error(f"Erreur fichier : {file_err}")
                flash("Erreur lors du traitement de l'image.", "danger")

            except OSError as os_err:
                current_app.logger.error(f"Erreur système : {os_err}")
                flash("Erreur système lors de la sauvegarde du fichier.", "danger")

            # --- En dernier recours ---
            except Exception as e:
                current_app.logger.exception(f"Erreur inattendue : {e}")
                flash("Une erreur interne est survenue pendant la création du service.", "danger")

        return render_template("service/create_service.html", form=form)

    @staticmethod
    def update_service(service_id):
        result = ServiceService.get_service_by_id(service_id)
        if not result.get("status"):
            flash(result.get("message", "Service introuvable."), "danger")
            return redirect(url_for('service.list_all_services'))

        service = result.get("service")
        form = ServiceUpdateForm(obj=service)

        if form.validate_on_submit():
            name = sanitize_html(form.name.data)
            description = sanitize_html(form.description.data)

            if detect_sql_injection(name) or detect_sql_injection(description):
                flash("Entrée invalide détectée.", "danger")
                return render_template("service/update_service.html", form=form, service=service)

            file = form.url_image.data
            url_image = service["url_image"]

            if isinstance(file, FileStorage) and file.filename:
                filename = secure_filename(file.filename)
                upload_dir = Path(current_app.config['SERVICE_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)

                filepath = upload_dir / filename
                file.save(filepath)
                url_image = f"uploads/service_img/{filename}"

            result = ServiceService.update_service(service_id, name, url_image, description)
            if result.get("status"):
                flash("Service mis à jour avec succès.", "success")
                return redirect(url_for('service.list_all_services'))
            else:
                flash(result.get("message", "Erreur lors de la mise à jour."), "danger")

        return render_template('service/update_service.html', form=form, service=service)

    @staticmethod
    def delete_service(service_id):
        result = ServiceService.delete_service(service_id)
        if result.get("status"):
            flash("Service supprimé avec succès.", "success")
        else:
            flash(result.get("message", "Erreur lors de la suppression."), "danger")
        return redirect(url_for('service.list_all_services'))






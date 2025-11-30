from flask import render_template, redirect, url_for, flash, current_app
from pathlib import Path
from werkzeug.utils import secure_filename
from app.forms.service_forms import ServiceCreateForm, ServiceUpdateForm
from app.services.service_service import ServiceService
from app.utils.security import sanitize_html
import uuid

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return f"{uuid.uuid4().hex}.{ext}"

class ServiceController:


# ======================================================
# LIST ALL SERVICES
# ======================================================
    @staticmethod
    def list_all_services():
        services = ServiceService.list_all_services()
        return render_template("service/list_all_services.html", services=services)

    # ======================================================
    # GET SERVICE BY ID
    # ======================================================
    @staticmethod
    def get_service_by_id(service_id):
        service, error = ServiceService.get_service_by_id(service_id)
        if error:
            flash(error, "danger")
            return redirect(url_for("service.list_all_services"))
        return render_template("service/service_details.html", service=service)

    # ======================================================
    # CREATE SERVICE
    # ======================================================
    @staticmethod
    def create_service():
        form = ServiceCreateForm()
        if form.validate_on_submit():
            file = form.url_image.data
            url_image = None
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename.lower())
                filename = generate_unique_filename(filename)
                upload_dir = Path(current_app.config['SERVICE_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)
                filepath = upload_dir / filename
                file.save(filepath)
                url_image = f"uploads/service_img/{filename}"

            name = sanitize_html(form.name.data)
            description = sanitize_html(form.description.data)

            service, error = ServiceService.create_service(name, description, url_image)
            if error:
                flash(error, "danger")
            else:
                flash("Service créé avec succès.", "success")
                return redirect(url_for("service.list_all_services"))

        return render_template("service/create_service.html", form=form)

    # ======================================================
    # INSTANCE CONTROLLER
    # ======================================================
    def __init__(self, service_id):
        self.service = ServiceService(service_id)

    # ======================================================
    # UPDATE SERVICE
    # ======================================================
    def update_service(self):
        if not self.service.exists():
            flash("Service non trouvé.", "danger")
            return redirect(url_for("service.list_all_services"))

        form = ServiceUpdateForm(obj=self.service.service)
        if form.validate_on_submit():
            file = form.url_image.data
            url_image = self.service.service.url_image  # par défaut garder l'ancienne image

            if hasattr(file, "filename") and file.filename:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename.lower())
                    filename = generate_unique_filename(filename)
                    upload_dir = Path(current_app.config['SERVICE_IMG_FOLDER'])
                    upload_dir.mkdir(parents=True, exist_ok=True)
                    filepath = upload_dir / filename
                    file.save(filepath)
                    url_image = f"uploads/service_img/{filename}"
                else:
                    flash("Format d'image non autorisé.", "danger")
                    return render_template(
                        "service/update_service.html", form=form, service=self.service.service
                    )

            name = sanitize_html(form.name.data)
            description = sanitize_html(form.description.data)
            success, error = self.service.update_service(name, description, url_image)
            if success:
                flash("Service mis à jour avec succès.", "success")
                return redirect(url_for("service.list_all_services"))
            else:
                flash(error, "danger")

        return render_template("service/update_service.html", form=form, service=self.service.service)

    # ======================================================
    # DELETE SERVICE
    # ======================================================
    def delete_service(self):
        success, error = self.service.delete_service()
        if error:
            flash(error, "danger")
        else:
            flash("Service supprimé avec succès.", "success")
        return redirect(url_for("service.list_all_services"))


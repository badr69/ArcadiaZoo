# app/controllers/habitat_controller.py

from flask import render_template, redirect, url_for, flash, current_app
from pathlib import Path
from werkzeug.utils import secure_filename
from app.forms.habitat_forms import HabitatCreateForm, HabitatUpdateForm
from app.services.habitat_service import HabitatService
from app.utils.security import sanitize_html
import uuid

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return f"{uuid.uuid4().hex}.{ext}"


class HabitatController:

    # ======================================================
    # LIST ALL HABITATS
    # ======================================================
    @staticmethod
    def list_all_habitats():
        habitats = HabitatService.list_all_habitats()
        return render_template("habitat/list_all_habitats.html", habitats=habitats)

    # ======================================================
    # GET HABITAT BY ID
    # ======================================================
    @staticmethod
    def get_habitat_by_id(habitat_id):
        service, error = HabitatService.get_habitat_by_id(habitat_id)
        if error:
            flash(error, "danger")
            return redirect(url_for("habitat.list_all_habitats"))
        return render_template("habitat/habitat_details.html", habitat=service)

    # ======================================================
    # CREATE HABITAT
    # ======================================================
    @staticmethod
    def create_habitat():
        form = HabitatCreateForm()
        if form.validate_on_submit():
            file = form.url_image.data
            url_image = None
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename.lower())
                filename = generate_unique_filename(filename)
                upload_dir = Path(current_app.config['HABITAT_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)
                filepath = upload_dir / filename
                file.save(filepath)
                url_image = f"uploads/habitat_img/{filename}"

            name = sanitize_html(form.name.data)
            description = sanitize_html(form.description.data)

            service, error = HabitatService.create_habitat(name, url_image, description)
            if error:
                flash(error, "danger")
            else:
                flash("Habitat créé avec succès.", "success")
                return redirect(url_for("habitat.list_all_habitats"))

        return render_template("habitat/create_habitat.html", form=form)

    # ======================================================
    # INSTANCE CONTROLLER
    # ======================================================
    def __init__(self, habitat_id):
        self.service = HabitatService(habitat_id)

    # ======================================================
    # UPDATE HABITAT
    # ======================================================
    def update_habitat(self):
        if not self.service.exists():
            flash("Habitat non trouvé.", "danger")
            return redirect(url_for("habitat.list_all_habitats"))

        form = HabitatUpdateForm(obj=self.service.habitat)
        if form.validate_on_submit():
            file = form.url_image.data
            url_image = self.service.habitat.url_image  # par défaut garder l'ancienne image

            if hasattr(file, "filename") and file.filename:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename.lower())
                    filename = generate_unique_filename(filename)
                    upload_dir = Path(current_app.config['HABITAT_IMG_FOLDER'])
                    upload_dir.mkdir(parents=True, exist_ok=True)
                    filepath = upload_dir / filename
                    file.save(filepath)
                    url_image = f"uploads/habitat_img/{filename}"
                else:
                    flash("Format d'image non autorisé.", "danger")
                    return render_template(
                        "habitat/update_habitat.html", form=form, habitat=self.service.habitat
                    )

            name = sanitize_html(form.name.data)
            description = sanitize_html(form.description.data)
            success, error = self.service.update_habitat(name, url_image, description)
            if success:
                flash("Habitat mis à jour avec succès.", "success")
                return redirect(url_for("habitat.list_all_habitats"))
            else:
                flash(error, "danger")

        return render_template("habitat/update_habitat.html", form=form, habitat=self.service.habitat)

    # ======================================================
    # DELETE HABITAT
    # ======================================================
    def delete_habitat(self):
        success, error = self.service.delete_habitat()
        if error:
            flash(error, "danger")
        else:
            flash("Habitat supprimé avec succès.", "success")
        return redirect(url_for("habitat.list_all_habitats"))

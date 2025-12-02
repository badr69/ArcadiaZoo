from flask import render_template, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid

from app.forms.animal_forms import AnimalCreateForm, AnimalUpdateForm
from app.services.animal_service import AnimalService
from app.utils.security import sanitize_html

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    ext = filename.rsplit('.',1)[1].lower()
    return f"{uuid.uuid4().hex}.{ext}"

class AnimalController:


    @staticmethod
    def list_all_animals():
        animals = AnimalService.list_all_animals()
        return render_template("animal/list_all_animals.html", animals=animals)

    @staticmethod
    def get_animal_by_id(animal_id):
        service, error = AnimalService.get_animal_by_id(animal_id)
        if error:
            flash(error, "danger")
            return redirect(url_for("animal.list_all_animals"))
        return render_template("animal/animal_details.html", animal=service)

    @staticmethod
    def create_animal():
        form = AnimalCreateForm()
        if form.validate_on_submit():
            file = form.url_image.data
            url_image = None
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename.lower())
                filename = generate_unique_filename(filename)
                upload_dir = Path(current_app.config['ANIMAL_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)
                file.save(upload_dir / filename)
                url_image = f"uploads/animal_img/{filename}"

            name = sanitize_html(form.name.data)
            race = sanitize_html(form.race.data)
            description = sanitize_html(form.description.data)
            habitat_id = form.habitat.data

            service, error = AnimalService.create_animal(name, race, description, url_image, habitat_id)
            if error:
                flash(error, "danger")
            else:
                flash("Animal créé avec succès.", "success")
                return redirect(url_for("animal.list_all_animals"))
        return render_template("animal/create_animal.html", form=form)

    def __init__(self):
        pass

    def update_animal(self, animal_id):
        # Instancie le service pour l'animal ciblé
        service = AnimalService(animal_id)
        if not service.exists():
            flash("Animal non trouvé.", "danger")
            return redirect(url_for("animal.list_all_animals"))

        # Crée le formulaire pré-rempli avec les données actuelles de l'animal
        form = AnimalUpdateForm(obj=service.animal)
        form.habitat.data = service.animal.habitat_id  # sélectionne le bon habitat

        if form.validate_on_submit():
            # Gestion de l'image
            file = form.url_image.data
            url_image = service.animal.url_image  # valeur par défaut

            if file and hasattr(file, "filename") and file.filename:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename.lower())
                    filename = generate_unique_filename(filename)
                    upload_dir = Path(current_app.config['ANIMAL_IMG_FOLDER'])
                    upload_dir.mkdir(parents=True, exist_ok=True)
                    file.save(upload_dir / filename)
                    url_image = f"uploads/animal_img/{filename}"
                else:
                    flash("Format d'image non autorisé.", "danger")
                    return render_template("animal/update_animal.html", form=form, animal=service.animal)

            # Récupération des autres champs
            name = sanitize_html(form.name.data)
            race = sanitize_html(form.race.data)
            description = sanitize_html(form.description.data)
            habitat_id = form.habitat.data

            # Appel du service pour la mise à jour
            success, error = service.update_animal(name, race, description, url_image, habitat_id)
            if success:
                flash("Animal mis à jour avec succès.", "success")
                return redirect(url_for("animal.list_all_animals"))
            else:
                flash(error, "danger")

        # Affiche le formulaire avec les données actuelles de l'animal
        return render_template("animal/update_animal.html", form=form, animal=service.animal)

    def delete_animal(self, animal_id):
        service = AnimalService(animal_id)
        success, error = service.delete_animal()
        if error:
            flash(error, "danger")
        else:
            flash("Animal supprimé avec succès.", "success")
        return redirect(url_for("animal.list_all_animals"))
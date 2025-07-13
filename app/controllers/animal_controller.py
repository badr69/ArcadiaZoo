import os
from pathlib import Path
from app.forms import AnimalCreateForm, AnimalUpdateForm
from app.services.animal_service import AnimalService
from flask import render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app
from werkzeug.datastructures import FileStorage



class AnimalController:
    @staticmethod
    def list_all_animals():
        animals = AnimalService.list_all_animals()
        return render_template('animal/list_all_animals.html', animals=animals)

    @staticmethod
    def get_animal_by_id(animal_id):
        animal = AnimalService.get_animal_by_id(animal_id)
        if animal is None:
            flash("animal non trouvé.", "danger")
            return redirect(url_for('animal.list_all_animals'))
        return render_template('animal/animal_details.html', animal=animal)



    @staticmethod
    def create_animal():
        form = AnimalCreateForm()

        # Debug éventuel (à supprimer en production)
        current_app.logger.debug("Form errors: %s", form.errors)

        if form.validate_on_submit():
            name = form.name.data
            description = form.description.data
            file = form.url_image.data  # FileStorage ou None

            # 1) Vérifier qu’un fichier a bien été téléversé
            if not file or file.filename == "":
                flash("Veuillez ajouter une image.", "danger")
                return render_template("animal/create_animal.html", form=form)

            # 2) Sauvegarder l’image
            try:
                filename = secure_filename(file.filename)
                upload_dir = Path(current_app.root_path) / "static" / "uploads"
                upload_dir.mkdir(parents=True, exist_ok=True)

                filepath = upload_dir / filename
                file.save(filepath)

                # Chemin à enregistrer en BDD
                url_image = f"/static/uploads/{filename}"

                # 3) Appeler le animal
                result = AnimalService.create_animal(
                    name=name,
                    url_image=url_image,
                    description=description
                )

                if result.get("status"):
                    flash("animal créé avec succès.", "success")
                    return redirect(url_for("animal.list_all_animals"))

                flash(result.get("message", "Erreur inconnue lors de la création."), "danger")

            except Exception:
                current_app.logger.exception("Erreur lors de la création de l'animal")
                flash("Une erreur est survenue pendant la création de l’animal.", "danger")

        # GET initial ou formulaire invalide
        return render_template("animal/create_animal.html", form=form)



    @staticmethod
    def update_animal(animal_id):
        animal = AnimalService.get_animal_by_id(animal_id)
        if animal is None:
            flash("animal non trouvé.", "danger")
            return redirect(url_for('animal.list_all_animals'))

        form = AnimalUpdateForm(obj=animal)

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
                url_image = animal.url_image  # garder l'image existante

            result = AnimalService.update_animal(animal_id, name, description, url_image)
            if result['status']:
                flash("animal mis à jour.", "success")
                return redirect(url_for('animal.list_all_animals'))
            else:
                flash(result['message'], "danger")

        return render_template('animal/update_animal.html', form=form, animal=animal)

    @staticmethod
    def delete_animal(animal_id):
        result = AnimalService.delete_animal(animal_id)
        if result['status']:
            flash("animal supprimé.", "success")
        else:
            flash(result['message'], "danger")
        return redirect(url_for('animal.list_all_animals'))

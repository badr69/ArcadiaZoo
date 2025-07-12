import os
from flask import render_template, request, redirect, url_for, flash
from app.services.animal_service import AnimalService
from flask import current_app
from app.forms import AnimalCreateForm, AnimalUpdateForm
from app.utils.allowedfiles import allowed_file
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileAllowed, FileRequired

class AnimalController:
    @staticmethod
    def list_all_animals():
        animals = AnimalService.list_all_animals()
        return render_template('animal/list_all_animals.html', animals=animals)


    @staticmethod

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

    @staticmethod
    def create_animal():
        form = AnimalCreateForm()

        if form.validate_on_submit():
            name = form.name.data
            race = form.race.data
            habitat_id = form.habitat.data
            image_paths = []

            if form.url_images.data:
                for file in form.url_images.data:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        upload_folder = current_app.config['UPLOAD_FOLDER']
                        os.makedirs(upload_folder, exist_ok=True)
                        path = os.path.join(upload_folder, filename)
                        file.save(path)
                        image_paths.append(path)

            # Pour simplifier, on prend le premier fichier si plusieurs
            url_image = image_paths[0] if image_paths else None

            result = AnimalService.create_animal(name, race, url_image, habitat_id)
            if result["status"]:
                flash("Animal ajouté avec succès.", "success")
                return redirect(url_for('animal_bp.list_animals'))
            else:
                flash(result["message"], "danger")

        return render_template("animal/create_animal.html", form=form)

    @staticmethod
    def get_animal_by_id(animal_id):
        animal = AnimalService.get_animal_by_id(animal_id)
        if not animal:
            flash("Animal introuvable.", "warning")
            return redirect(url_for('animal_bp.list_animals'))
        if request.method == 'POST':
            name = request.form['name']
            race = request.form['species']
            success = AnimalService.update_animal(animal_id, name, race)
            if success:
                flash("Animal modifié avec succès.", "success")
            else:
                flash("Erreur lors de la modification.", "danger")
            return redirect(url_for('animal_bp.list_all_animals'))
        return render_template('animal/animal_detail.html', animal=animal)


    @staticmethod
    def update_animal(animal_id):
        animal = AnimalService.get_animal_by_id(animal_id)
        if animal is None:
            flash("Habitat non trouvé.", "danger")
            return redirect(url_for('habitat.list_all_Animal'))

        form = AnimalUpdateForm(obj=animal)  # Pré-remplit le formulaire avec l'objet habitat

        if form.validate_on_submit():
            name = form.name.data
            race = form.race.data
            # Gestion des images uploadées
            files = form.url_images.data
            if files:
                # Traite le premier fichier pour l'exemple
                file = files[0]
                if file:
                    filename = secure_filename(file.filename)
                    upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
                    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                    file.save(upload_path)
                    url_image = f'/static/uploads/{filename}'
            else:
                url_image = animal.url_images  # garder l'ancienne image

            # Appeler la mise à jour dans le service
            result = AnimalService.update_animal(animal_id, name, race, url_images)
            if result['status']:
                flash("Habitat mis à jour.", "success")
                return redirect(url_for('habitat.list_all_habitats'))
            else:
                flash(result['message'], "danger")

        return render_template('habitat/update_habitat.html', form=form, animal=animal)

    @staticmethod
    def delete_animal(animal_id):
        success = AnimalService.delete_animal(animal_id)
        if success:
            flash("Animal supprimé.", "success")
        else:
            flash("Erreur lors de la suppression.", "danger")
        return redirect(url_for('animal_bp.list_all_animals'))

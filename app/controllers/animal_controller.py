from flask import render_template, flash, redirect, url_for, request, current_app
from werkzeug.utils import secure_filename
from pathlib import Path
from app.forms.animal_forms import AnimalCreateForm, AnimalUpdateForm
from app.services.animal_service import AnimalService
from app.utils.security import sanitize_html, detect_sql_injection


class AnimalController:

    @classmethod
    def list_all_animals(cls):
        # TODO: Appeler le service pour récupérer tous les animaux
        result = AnimalService.list_all_animals()
        animals = result.get("data", [])
        # TODO: Afficher la liste dans la vue HTML
        return render_template('animal/list_all_animals.html', animals=animals)

    @classmethod
    def get_animal_by_id(cls, animal_id):
        # TODO: Récupérer un animal spécifique via son ID
        result = AnimalService.get_animal_by_id(animal_id)
        if not result["status"]:
            # TODO: Gérer le cas où l’animal n’existe pas (flash message + redirection)
            flash(result["message"], "danger")
            return redirect(url_for("animal.list_all_animals"))
        # TODO: Afficher les détails de l’animal dans la vue
        return render_template('animal/animal_details.html', animal=result["data"])

    @classmethod
    def create_animal(cls):
        # TODO: Instancier le formulaire de création
        form = AnimalCreateForm()

        if form.validate_on_submit():
            # TODO: Nettoyer les champs texte pour éviter XSS
            name = sanitize_html(form.name.data)
            race = sanitize_html(form.race.data)
            description = sanitize_html(form.description.data)
            file = form.url_image.data

            # TODO: Protection contre injection SQL
            if detect_sql_injection(name) or detect_sql_injection(race) or detect_sql_injection(description):
                flash("Entrée invalide détectée.", "danger")
                return render_template("animal/create_animal.html", form=form)

            # TODO: Vérifier la présence d’une image
            if not file or file.filename == "":
                flash("Veuillez ajouter une image.", "danger")
                return render_template("animal/create_animal.html", form=form)

            try:
                # TODO: Sécuriser le nom de fichier pour éviter path traversal
                filename = secure_filename(file.filename)
                # TODO: Créer le dossier d’upload s’il n’existe pas
                upload_dir = Path(current_app.config['ANIMAL_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)
                # TODO: Enregistrer le fichier sur le serveur
                filepath = upload_dir / filename
                file.save(filepath)
                url_image = f"uploads/animal_img/{filename}"

                # TODO: Appeler le service pour créer l’animal en base
                result = AnimalService.create_animal(name, race, description, url_image)
                if result["status"]:
                    flash("Animal créé avec succès !", "success")
                    return redirect(url_for("animal.list_all_animals"))
                flash(result.get("message", "Erreur inconnue."), "danger")

            except Exception:
                # TODO: Log et message d’erreur en cas d’exception lors de la création
                current_app.logger.exception("Erreur lors de la création de l'animal.")
                flash("Erreur lors de la création de l'animal.", "danger")

        # TODO: Afficher le formulaire (GET ou erreur validation)
        return render_template("animal/create_animal.html", form=form)

    @classmethod
    def update_animal(cls, animal_id):
        # TODO: Récupérer l’animal pour pré-remplir le formulaire
        result = AnimalService.get_animal_by_id(animal_id)
        if not result["status"]:
            flash(result["message"], "danger")
            return redirect(url_for("animal.list_all_animals"))

        animal = result["data"]
        form = AnimalUpdateForm(data={
            "name": animal.name,
            "race": animal.race,
            "description": animal.description
        })

        if form.validate_on_submit():
            # TODO: Nettoyer les champs texte pour éviter XSS
            name = sanitize_html(form.name.data)
            race = sanitize_html(form.race.data)
            description = sanitize_html(form.description.data)
            file = form.url_image.data

            # TODO: Protection contre injection SQL
            if detect_sql_injection(name) or detect_sql_injection(race) or detect_sql_injection(description):
                flash("Entrée invalide détectée.", "danger")
                return render_template("animal/update_animal.html", form=form, animal=animal)

            # TODO: Gestion optionnelle du fichier image (upload nouveau fichier ou garder l’ancien)
            url_image = animal.url_image
            if file and file.filename != "":
                filename = secure_filename(file.filename)
                upload_dir = Path(current_app.config['ANIMAL_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)
                filepath = upload_dir / filename
                file.save(filepath)
                url_image = f"uploads/animal_img/{filename}"

            # TODO: Appeler le service pour mettre à jour l’animal
            update_result = AnimalService.update_animal(animal_id, name, race, description, url_image)
            if update_result["status"]:
                flash("Animal mis à jour avec succès !", "success")
                return redirect(url_for("animal.list_all_animals"))
            flash(update_result["message"], "danger")

        # TODO: Afficher le formulaire avec les données existantes en GET ou si erreur validation
        return render_template("animal/update_animal.html", form=form, animal=animal)

    @classmethod
    def delete_animal(cls, animal_id):
        if request.method == "POST":
            # TODO: Appeler le service pour supprimer l’animal
            result = AnimalService.delete_animal(animal_id)
            if result["status"]:
                flash("Animal supprimé avec succès !", "success")
            else:
                flash(result["message"], "danger")
            # TODO: Rediriger vers la liste après suppression
            return redirect(url_for("animal.list_all_animals"))

        # Confirmation avant suppression
        result = AnimalService.get_animal_by_id(animal_id)
        if not result["status"]:
            flash(result["message"], "danger")
            return redirect(url_for("animal.list_all_animals"))
        animal = result["data"]
        return render_template("animal/delete_confirm.html", animal=animal)


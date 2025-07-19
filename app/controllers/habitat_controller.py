import os
from pathlib import Path
from app.forms.habitat_forms import HabitatCreateForm, HabitatUpdateForm
from app.services.habitat_service import HabitatService
from flask import render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app


class HabitatController:
    @staticmethod
    def list_all_habitats():
        habitats = HabitatService.list_all_habitats()
        return render_template('habitat/list_all_habitats.html', habitats=habitats)

    @staticmethod
    def get_habitat_by_id(habitat_id):
        habitat = HabitatService.get_habitat_by_id(habitat_id)
        if habitat is None:
            flash("Habitat non trouvé.", "danger")
            return redirect(url_for('habitat.list_habitats'))
        return render_template('habitat/habitat_details.html', habitat=habitat)

    @staticmethod
    def create_habitat():
        form = HabitatCreateForm()

        # Debug éventuel (à supprimer en production)
        current_app.logger.debug("Form errors: %s", form.errors)

        if form.validate_on_submit():
            name = form.name.data
            file = form.url_image.data  # FileStorage ou None
            description = form.description.data

            # 1) Vérifier qu’un fichier a bien été téléversé
            if not file or file.filename == "":
                flash("Veuillez ajouter une image.", "danger")
                return render_template("habitat/create_habitat.html", form=form)

            # 2) Sauvegarder l’image
            try:
                filename = secure_filename(file.filename)
                upload_dir = Path(current_app.config['HABITAT_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)

                filepath = upload_dir / filename
                file.save(filepath)

                # Chemin à enregistrer en BDD
                url_image = f"uploads/habitat_img/{filename}"

                # 3) Appeler le service
                result = HabitatService.create_habitat(
                    name=name,
                    url_image=url_image,
                    description=description
                )

                if result.get("status"):
                    flash("Habitat créé avec succès.", "success")
                    return redirect(url_for("habitat.list_all_habitats"))

                flash(result.get("message", "Erreur inconnue lors de la création."), "danger")

            except Exception:
                current_app.logger.exception("Erreur lors de la création de l'habitat")
                flash("Une erreur est survenue pendant la création de l’habitat.", "danger")

        # GET initial ou formulaire invalide
        return render_template("habitat/create_habitat.html", form=form)

    @staticmethod
    def update_habitat(habitat_id):
        habitat = HabitatService.get_habitat_by_id(habitat_id)
        if habitat is None:
            flash("Habitat non trouvé.", "danger")
            return redirect(url_for('habitat.list_all_habitats'))

        form = HabitatUpdateForm(obj=habitat)  # Pré-remplit le formulaire avec l'objet habitat

        if form.validate_on_submit():
            name = form.name.data
            description = form.description.data

            file = form.url_image.data
            if hasattr(file, 'filename') and file.filename != '':
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                file.save(upload_path)
                url_image = f'/static/uploads/{filename}'
            else:
                url_image = habitat.url_image  # garder l'ancienne image

            # Appeler la mise à jour dans le service
            result = HabitatService.update_habitat(habitat_id, name, description, url_image)
            if result['status']:
                flash("Habitat mis à jour.", "success")
                return redirect(url_for('habitat.list_all_habitats'))
            else:
                flash(result['message'], "danger")

        return render_template('habitat/update_habitat.html', form=form, habitat=habitat)

    @staticmethod
    def delete_habitat(habitat_id):
        result = HabitatService.delete_habitat(habitat_id)
        if result['status']:
            flash("Habitat supprimé.", "success")
        else:
            flash(result['message'], "danger")
        return redirect(url_for('habitat.list_all_habitats'))

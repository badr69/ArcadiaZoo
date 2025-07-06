import os
from app.forms import HabitatCreateForm, HabitatUpdateForm
from app.services.habitats_service import HabitatService
from flask import render_template, request, redirect, url_for, flash
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

        if request.method == 'POST' and form.validate_on_submit():
            name = form.name.data
            description = form.description.data

            # Traitement de l'image
            file = request.files.getlist('images')[0] if request.files.getlist('images') else None
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                file.save(upload_path)
                url_image = f'/static/uploads/{filename}'
            else:
                flash("Veuillez ajouter au moins une image.", "danger")
                return render_template('habitat/create_habitat.html', form=form)

            result = HabitatService.create_habitat(name, url_image, description)
            if result['status']:
                flash("Habitat créé avec succès.", "success")
                return redirect(url_for('habitat.list_all_habitats'))
            else:
                flash(result['message'], "danger")

        return render_template('habitat/create_habitat.html', form=form)


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
                url_image = habitat.url_image  # garder l'ancienne image

            # Appeler la mise à jour dans le service
            result = HabitatService.update_habitat(habitat_id, name, url_image, description)
            if result['status']:
                flash("Habitat mis à jour.", "success")
                return redirect(url_for('habitat.list_all_habitats'))
            else:
                flash(result['message'], "danger")

        return render_template('habitat/update_habitat.html', form=form, habitat=habitat)

    # def update_habitat(habitat_id):
    #     habitat = HabitatService.get_habitat_by_id(habitat_id)
    #     if habitat is None:
    #         flash("Habitat non trouvé.", "danger")
    #         return redirect(url_for('habitat.list_habitats'))
    #
    #     if request.method == 'POST':
    #         name = request.form.get('name')
    #         url_image = request.form.get('url_image')
    #         description = request.form.get('description')
    #         result = HabitatService.update_habitat(habitat_id, name, url_image, description)
    #         if result['status']:
    #             flash("Habitat mis à jour.", "success")
    #             return redirect(url_for('habitat.update_habitat', habitat_id=habitat_id))
    #         else:
    #             flash(result['message'], "danger")
    #
    #     return render_template('habitat/habitat_details.html', habitat=habitat)

    @staticmethod
    def delete_habitat(habitat_id):
        result = HabitatService.delete_habitat(habitat_id)
        if result['status']:
            flash("Habitat supprimé.", "success")
        else:
            flash(result['message'], "danger")
        return redirect(url_for('habitat.list_all_habitats'))

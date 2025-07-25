import uuid
from pathlib import Path
from app.forms.animal_forms import AnimalCreateForm, AnimalUpdateForm
from app.services.animal_service import AnimalService
from flask import render_template, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from app.utils.security import detect_sql_injection, sanitize_html


class AnimalController:
    @staticmethod
    def list_all_animals():
        animals = AnimalService.list_all_animals()
        return render_template('animal/list_all_animals.html', animals=animals)

    @staticmethod
    def get_animal_by_id(animal_id):
        animal = AnimalService.get_animal_by_id(animal_id)
        if animal is None:
            flash("Animal non trouvé.", "danger")
            return redirect(url_for('animal.list_all_animals'))
        return render_template('animal/animal_details.html', animal=animal)


    @staticmethod
    def create_animal():
        form = AnimalCreateForm()

        current_app.logger.debug("Form errors: %s", form.errors)

        if form.validate_on_submit():
            name = sanitize_html(form.name.data)
            race = sanitize_html(form.race.data)
            description = sanitize_html(form.description.data)
            file = form.url_image.data

            if detect_sql_injection(name) or detect_sql_injection(race) or detect_sql_injection(description):
                flash("Invalide Input.", "danger")
                return render_template("animal/create_animal.html", form=form)

            if not file or file.filename == "":
                flash("Please add an image.", "danger")
                return render_template("animal/create_animal.html", form=form)

            try:
                filename = secure_filename(file.filename)
                upload_dir = Path(current_app.config['ANIMAL_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)

                filepath = upload_dir / filename
                file.save(filepath)

                url_image = f"uploads/animal_img/{filename}"

                result = AnimalService.create_animal(
                    name=name,
                    race=race,
                    description=description,
                    url_image=url_image
                )

                if result.get("status"):
                    flash("Animal created with success.", "success")
                    return redirect(url_for("animal.list_all_animals"))

                flash(result.get("message", "Unknoun Error when Creation."), "danger")

            except Exception:
                current_app.logger.exception("Error when creating animal")
                flash("Error when creating animal.", "danger")

        return render_template("animal/create_animal.html", form=form)

    @staticmethod
    def update_animal(animal_id):
        animal = AnimalService.get_animal_by_id(animal_id)
        if animal is None:
            flash("Animal not found.", "danger")
            return redirect(url_for('animal.list_all_animals'))

        form = AnimalUpdateForm(obj=animal)

        if form.validate_on_submit():
            name = sanitize_html(form.name.data)
            race = sanitize_html(form.race.data)
            description = sanitize_html(form.description.data)

            if detect_sql_injection(name) or detect_sql_injection(race) or detect_sql_injection(description):
                flash("Invalide Input.", "danger")
                return render_template("animal/create_animal.html", form=form)

            file = form.url_image.data

            if isinstance(file, FileStorage) and file.filename:
                filename = secure_filename(file.filename)
                upload_path = Path(current_app.root_path) / 'static' / 'uploads' / filename
                upload_path.parent.mkdir(parents=True, exist_ok=True)
                file.save(upload_path)
                url_image = f'uploads/animal_img/{filename}'
            else:
                url_image = animal.url_image

            result = AnimalService.update_animal(animal_id, name, race, description, url_image)
            if result['status']:
                flash("Animal Updated with success.", "success")
                return redirect(url_for('animal.list_all_animals'))
            else:
                flash(result['message'], "danger")

        return render_template('animal/update_animal.html', form=form, animal=animal)

    @staticmethod
    def delete_animal(animal_id):
        result = AnimalService.delete_animal(animal_id)
        if result['status']:
            flash("Animal supprimé.", "success")
        else:
            flash(result['message'], "danger")
        return redirect(url_for('animal.list_all_animals'))

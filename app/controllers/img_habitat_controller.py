from pathlib import Path
from app.forms.img_habitat_form import ImgHabitatCreateForm, ImgHabitatUpdateForm
from app.services.img_habitat_service import ImgHabitatService
from flask import render_template, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from app.utils.security import detect_sql_injection, sanitize_html


class ImgHabitatController:
    @staticmethod
    def get_all():
        images = ImgHabitatService.get_all()
        return render_template('img_habitat/list_all.html', images=images)

    @staticmethod
    def get_by_id(image_id):
        try:
            image = ImgHabitatService.get_by_id(image_id)
            return render_template('img_habitat/details.html', image=image)
        except LookupError:
            flash("Image non trouvée.", "danger")
            return redirect(url_for('img_habitat.list_all'))

    @staticmethod
    def create():
        form = ImgHabitatCreateForm()

        if form.validate_on_submit():
            name = form.name.data
            description = sanitize_html(form.description.data)
            file = form.filename.data

            if detect_sql_injection(name) or detect_sql_injection(description):
                flash("Entrée invalide détectée.", "danger")
                return render_template("img_habitat/create.html", form=form)

            if not file or not hasattr(file, 'filename') or file.filename == '':
                flash("Aucun fichier sélectionné.", "danger")
                return render_template("img_habitat/create.html", form=form)

            try:
                filename = secure_filename(file.filename)
                upload_dir = Path(current_app.config['HABITAT_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)
                filepath = upload_dir / filename
                file.save(filepath)

                file_url = f"uploads/img_habitat/{filename}"

                ImgHabitatService.create(name, file_url, description)

                flash("Image ajoutée avec succès.", "success")
                return redirect(url_for("img_habitat.list_all"))

            except Exception:
                current_app.logger.exception("Erreur lors de l’ajout de l'image")
                flash("Une erreur est survenue pendant l’ajout.", "danger")

        return render_template("img_habitat/create.html", form=form)

    @staticmethod
    def update(image_id):
        try:
            img = ImgHabitatService.get_by_id(image_id)
        except LookupError:
            flash("Image non trouvée.", "danger")
            return redirect(url_for('img_habitat.list_all'))

        form = ImgHabitatUpdateForm(obj=img)

        if form.validate_on_submit():
            name = form.name.data
            description = sanitize_html(form.description.data)
            file = form.filename.data

            if detect_sql_injection(name) or detect_sql_injection(description):
                flash("Entrée invalide détectée.", "danger")
                return render_template("img_habitat/update.html", form=form)

            if file and hasattr(file, 'filename') and file.filename != '':
                filename = secure_filename(file.filename)
                upload_dir = Path(current_app.config['HABITAT_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)
                filepath = upload_dir / filename
                file.save(filepath)
                file_url = f"uploads/img_habitat/{filename}"
            else:
                file_url = img.filename

            try:
                ImgHabitatService.update(image_id, name, file_url, description)
                flash("Image mise à jour avec succès.", "success")
                return redirect(url_for('img_habitat.list_all'))
            except Exception as e:
                current_app.logger.exception("Erreur lors de la mise à jour de l'image")
                flash("Une erreur est survenue pendant la mise à jour.", "danger")
                return render_template("img_habitat/update.html", form=form)

        return render_template("img_habitat/update.html", form=form)

    @staticmethod
    def delete(image_id):
        try:
            ImgHabitatService.delete(image_id)
            flash("Image supprimée avec succès.", "success")
        except LookupError:
            flash("Image non trouvée.", "danger")
        except Exception:
            current_app.logger.exception("Erreur lors de la suppression de l'image")
            flash("Une erreur est survenue pendant la suppression.", "danger")
        return redirect(url_for('img_habitat.list_all'))

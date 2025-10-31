from pathlib import Path
from flask import render_template, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import psycopg2
import mimetypes
import logging

from app.forms.habitat_forms import HabitatCreateForm, HabitatUpdateForm
from app.services.habitat_service import HabitatService
from app.utils.security import detect_sql_injection, sanitize_html

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class HabitatController:
    @classmethod
    def list_all_habitats(cls):
        habitats = HabitatService.list_all_habitats()
        return render_template('habitat/list_all_habitats.html', habitats=habitats)


    @classmethod
    def get_habitat_by_id(cls, habitat_id):
        habitat = HabitatService.get_habitat_by_id(habitat_id)
        if habitat is None:
            flash("Habitat non trouvé.", "danger")
            return redirect(url_for('habitat.list_all_habitats'))
        return render_template('habitat/habitat_details.html', habitat=habitat)

    @classmethod
    def create_habitat(cls):
        form = HabitatCreateForm()

        if form.validate_on_submit():
            name = sanitize_html(form.name.data)
            file = form.url_image.data
            description = sanitize_html(form.description.data)

            if detect_sql_injection(name) or detect_sql_injection(description):
                flash("Input invalide.", "danger")
                return render_template("habitat/create_habitat.html", form=form)

            if not file or file.filename == "":
                flash("Veuillez ajouter une image.", "danger")
                return render_template("habitat/create_habitat.html", form=form)

            if not allowed_file(file.filename):
                flash("Format d'image non autorisé. Seuls PNG, JPG, JPEG, GIF sont acceptés.", "danger")
                return render_template("habitat/create_habitat.html", form=form)

            try:
                filename = secure_filename(file.filename)
                upload_dir = Path(current_app.config['HABITAT_IMG_FOLDER'])
                upload_dir.mkdir(parents=True, exist_ok=True)
                filepath = upload_dir / filename

                # Vérification du MIME type pour plus de sécurité
                mimetype, _ = mimetypes.guess_type(filepath)
                if not mimetype or not mimetype.startswith("image/"):
                    flash("Le fichier uploadé n'est pas une image valide.", "danger")
                    return render_template("habitat/create_habitat.html", form=form)

                file.save(filepath)
                url_image = f"uploads/habitat_img/{filename}"

                result = HabitatService.create_habitat(
                    name=name,
                    url_image=url_image,
                    description=description
                )

                if result.get("status"):
                    flash("Habitat créé avec succès.", "success")
                    return redirect(url_for("habitat.list_all_habitats"))

                flash(result.get("message", "Erreur inconnue lors de la création."), "danger")

            except (OSError, psycopg2.DatabaseError) as e:
                logging.exception("Erreur technique lors de la création de l'habitat")
                flash(f"Erreur technique: {str(e)}", "danger")

            except HTTPException as e:
                logging.exception("Erreur HTTP")
                flash(f"Erreur HTTP: {str(e)}", "danger")

        return render_template("habitat/create_habitat.html", form=form)


    @classmethod
    def update_habitat(cls, habitat_id):
        habitat = HabitatService.get_habitat_by_id(habitat_id)
        if habitat is None:
            flash("Habitat non trouvé.", "danger")
            return redirect(url_for('habitat.list_all_habitats'))

        form = HabitatUpdateForm(obj=habitat)

        if form.validate_on_submit():
            name = sanitize_html(form.name.data)
            file = form.url_image.data
            description = sanitize_html(form.description.data)

            if detect_sql_injection(name) or detect_sql_injection(description):
                flash("Input invalide.", "danger")
                return render_template("habitat/update_habitat.html", form=form)

            try:
                url_image = habitat.url_image
                if hasattr(file, 'filename') and file.filename != '':
                    if not allowed_file(file.filename):
                        flash("Format d'image non autorisé.", "danger")
                        return render_template("habitat/update_habitat.html", form=form, habitat=habitat)

                    filename = secure_filename(file.filename)
                    upload_dir = Path(current_app.config['HABITAT_IMG_FOLDER'])
                    upload_dir.mkdir(parents=True, exist_ok=True)
                    filepath = upload_dir / filename

                    mimetype, _ = mimetypes.guess_type(filepath)
                    if not mimetype or not mimetype.startswith("image/"):
                        flash("Le fichier uploadé n'est pas une image valide.", "danger")
                        return render_template("habitat/update_habitat.html", form=form, habitat=habitat)

                    file.save(filepath)
                    url_image = f"uploads/habitat_img/{filename}"

                result = HabitatService.update_habitat(habitat_id, name, url_image, description)
                if result.get('status'):
                    flash("Habitat mis à jour avec succès.", "success")
                    return redirect(url_for("habitat.list_all_habitats"))
                flash(result.get("message", "Erreur inconnue lors de la mise à jour."), "danger")

            except (OSError, psycopg2.DatabaseError) as e:
                logging.exception("Erreur technique lors de la mise à jour")
                flash(f"Erreur technique: {str(e)}", "danger")

            except HTTPException as e:
                logging.exception("Erreur HTTP lors de la mise à jour")
                flash(f"Erreur HTTP: {str(e)}", "danger")

        return render_template("habitat/update_habitat.html", form=form, habitat=habitat)


    @classmethod
    def delete_habitat(cls, habitat_id):
        try:
            result = HabitatService.delete_habitat(habitat_id)
            if result.get('status'):
                flash("Habitat supprimé avec succès.", "success")
            else:
                flash(result.get('message', "Erreur lors de la suppression."), "danger")
        except psycopg2.DatabaseError as e:
            logging.exception("Erreur base de données lors de la suppression")
            flash(f"Erreur technique: {str(e)}", "danger")
        except HTTPException as e:
            logging.exception("Erreur HTTP lors de la suppression")
            flash(f"Erreur HTTP: {str(e)}", "danger")

        return redirect(url_for('habitat.list_all_habitats'))






# import os
# from pathlib import Path
# from app.forms.habitat_forms import HabitatCreateForm, HabitatUpdateForm
# from app.services.habitat_service import HabitatService
# from flask import render_template, redirect, url_for, flash
# from werkzeug.utils import secure_filename
# from flask import current_app
#
# from app.utils.security import detect_sql_injection, sanitize_html
#
#
# class HabitatController:
#     @staticmethod
#     def list_all_habitats():
#         habitats = HabitatService.list_all_habitats()
#         return render_template('habitat/list_all_habitats.html', habitats=habitats)
#
#     @staticmethod
#     def get_habitat_by_id(habitat_id):
#         habitat = HabitatService.get_habitat_by_id(habitat_id)
#         if habitat is None:
#             flash("Habitat non trouvé.", "danger")
#             return redirect(url_for('habitat.list_habitats'))
#         return render_template('habitat/habitat_details.html', habitat=habitat)
#
#     @staticmethod
#     def create_habitat():
#         form = HabitatCreateForm()
#         # Debug éventuel (à supprimer en production)
#         # current_app.logger.debug("Form errors: %s", form.errors)
#
#         if form.validate_on_submit():
#             name = sanitize_html(form.name.data)
#             file = form.url_image.data
#             description = sanitize_html(form.description.data)
#
#             if detect_sql_injection(name) or detect_sql_injection(description):
#                 flash("Invalide Input.", "danger")
#                 return render_template("habitat/create_habitat.html", form=form)
#
#             # 1) Vérifier qu’un fichier a bien été téléversé
#             if not file or file.filename == "":
#                 flash("Veuillez ajouter une image.", "danger")
#                 return render_template("habitat/create_habitat.html", form=form)
#
#             # 2) Sauvegarder l’image
#             try:
#                 filename = secure_filename(file.filename)
#                 upload_dir = Path(current_app.config['HABITAT_IMG_FOLDER'])
#                 upload_dir.mkdir(parents=True, exist_ok=True)
#
#                 filepath = upload_dir / filename
#                 file.save(filepath)
#
#                 # Chemin à enregistrer en BDD
#                 url_image = f"uploads/habitat_img/{filename}"
#
#                 # 3) Appeler le service
#                 result = HabitatService.create_habitat(
#                     name=name,
#                     url_image=url_image,
#                     description=description
#                 )
#
#                 if result.get("status"):
#                     flash("Habitat créé avec succès.", "success")
#                     return redirect(url_for("habitat.list_all_habitats"))
#
#                 flash(result.get("message", "Erreur inconnue lors de la création."), "danger")
#
#             except Exception:
#                 current_app.logger.exception("Erreur lors de la création de l'habitat")
#                 flash("Une erreur est survenue pendant la création de l’habitat.", "danger")
#
#         # GET initial ou formulaire invalide
#         return render_template("habitat/create_habitat.html", form=form)
#
#     @staticmethod
#     def update_habitat(habitat_id):
#         habitat = HabitatService.get_habitat_by_id(habitat_id)
#         if habitat is None:
#             flash("Habitat non trouvé.", "danger")
#             return redirect(url_for('habitat.list_all_habitats'))
#
#         form = HabitatUpdateForm(obj=habitat)  # Pré-remplit le formulaire avec l'objet habitat
#
#         if form.validate_on_submit():
#             name = sanitize_html(form.name.data)
#             file = form.url_image.data
#             description = sanitize_html(form.description.data)
#
#             if detect_sql_injection(name) or detect_sql_injection(description):
#                 flash("Invalide Input.", "danger")
#                 return render_template("habitat/update_habitat.html", form=form)
#
#
#             if hasattr(file, 'filename') and file.filename != '':
#                 filename = secure_filename(file.filename)
#                 upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
#                 os.makedirs(os.path.dirname(upload_path), exist_ok=True)
#                 file.save(upload_path)
#                 url_image = f'uploads/habitat_img/{filename}'
#             else:
#                 url_image = habitat.url_image  # garder l'ancienne image
#
#             # Appeler la mise à jour dans le service
#             result = HabitatService.update_habitat(habitat_id, name, url_image, description)
#             if result['status']:
#                 flash("Habitat mis à jour.", "success")
#                 return redirect(url_for('habitat.list_all_habitats'))
#             else:
#                 flash(result['message'], "danger")
#
#         return render_template('habitat/update_habitat.html', form=form, habitat=habitat)
#
#     @staticmethod
#     def delete_habitat(habitat_id):
#         result = HabitatService.delete_habitat(habitat_id)
#         if result['status']:
#             flash("Habitat supprimé.", "success")
#         else:
#             flash(result['message'], "danger")
#         return redirect(url_for('habitat.list_all_habitats'))

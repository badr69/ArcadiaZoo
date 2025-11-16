from flask import render_template, redirect, url_for, flash
from app.services.img_habitat_service import ImgHabitatService
from app.forms.img_habitat_forms import ImgHabitatCreateForm, ImgHabitatUpdateForm
from app.utils.security import sanitize_html, detect_sql_injection

class ImgHabitatController:

    @staticmethod
    def list_all_ha_img():
        images = ImgHabitatService.list_all_ha_img()
        return render_template("img_habitat/list_all_ha_img.html", images=images)

    @staticmethod
    def get_ha_img_by_id(img_ha_id):
        try:
            img = ImgHabitatService.get_ha_img_by_id(img_ha_id)
        except LookupError:
            flash("Image introuvable.", "danger")
            return redirect(url_for("img_habitat.list_all_ha_img"))
        return render_template("img_habitat/details_ha_img_.html", img=img)

    @staticmethod
    def create_ha_img():
        form = ImgHabitatCreateForm()
        if form.validate_on_submit():
            description = sanitize_html(form.description.data)
            file = form.image_file.data
            habitat_id = form.habitat_id.data

            if detect_sql_injection(description):
                flash("Input invalide.", "danger")
                return render_template("img_habitat/create_ha_img.html", form=form)

            try:
                ImgHabitatService.create_ha_img(habitat_id, file, description)
                flash("Image créée avec succès.", "success")
                return redirect(url_for("img_habitat.list_all_ha_img"))
            except Exception as e:
                flash(str(e), "danger")

        return render_template("img_habitat/create_ha_img.html", form=form)

    @staticmethod
    def update_ha_img(img_id):
        img = ImgHabitatService.get_ha_img_by_id(img_id)
        form = ImgHabitatUpdateForm(obj=img)

        if form.validate_on_submit():
            description = sanitize_html(form.description.data)
            file = form.image_file.data
            habitat_id = form.habitat_id.data

            try:
                ImgHabitatService.update_ha_img(img_id, habitat_id, file, description)
                flash("Image mise à jour.", "success")
                return redirect(url_for("img_habitat.list_all_ha_img"))
            except Exception as e:
                flash(str(e), "danger")

        return render_template("img_habitat/update_ha_img.html", form=form, img=img)

    @staticmethod
    def delete_ha_img(img_id):
        try:
            ImgHabitatService.delete(img_id)
            flash("Image supprimée.", "success")
        except Exception as e:
            flash(str(e), "danger")
        return redirect(url_for("img_habitat.list_all_ha_img"))

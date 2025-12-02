# app/controllers/care_controller.py
from flask import render_template, redirect, url_for, flash
from app.forms.care_forms import CareCreateForm, CareUpdateForm
from app.services.care_service import CareService

class CareController:
    """
    Controller pour gérer les routes liées aux soins (Care)
    """

    # ======================================================
    # LIST ALL CARES
    # ======================================================
    @staticmethod
    def list_all_cares():
        cares, error = CareService.list_all_cares()
        if error:
            flash(error, "danger")
        return render_template("care/list_all_cares.html", cares=cares)

    @staticmethod
    def get_care_by_id(care_id):
        """
        Récupère un soin par son ID et le passe au template.
        """
        care, error = CareService.get_care_by_id(care_id)
        if error:
            # Par exemple, afficher un message d'erreur dans un template
            return render_template("care/care_details.html", care=None, error=error)

        return render_template("care/care_details.html", care=care, error=None)

    # ======================================================
    # CREATE CARE
    # ======================================================
    @staticmethod
    def create_care():
        form = CareCreateForm()
        if form.validate_on_submit():
            care, error = CareService.create_care(
                animal_id=form.animal_id.data,
                user_id=form.user_id.data,
                type_care=form.type_care.data,
                description=form.description.data,
                date_care=form.date_care.data
            )
            if error:
                flash(error, "danger")
            else:
                flash("Soin créé avec succès.", "success")
                return redirect(url_for("care.list_all_cares"))
        return render_template("care/create_care.html", form=form)

    # ======================================================
    # UPDATE CARE
    # ======================================================

    @staticmethod
    def update_care(care_id):
        care_service = CareService(care_id)
        if not care_service.exists():
            flash("Soin introuvable.", "danger")
            return redirect(url_for("care.list_all_cares"))
        form = CareUpdateForm(obj=care_service.care)  # pré-remplit le formulaire avec l'objet

        if form.validate_on_submit():
            success, message = care_service.update_care(
                animal_id=form.animal_id.data,
                user_id=form.user_id.data,
                type_care=form.type_care.data,
                description=form.description.data,
                date_care=form.date_care.data
            )
            if success:
                flash("Soin mis à jour avec succès.", "success")
                return redirect(url_for("care.list_all_cares"))
            else:
                flash(message, "danger")

        return render_template("care/update_care.html", form=form, care=care_service.care)

    # ======================================================
    # DELETE CARE
    # ======================================================
    @staticmethod
    def delete_care(care_id):
        care_service = CareService(care_id)
        if not care_service.exists():
            flash("Soin introuvable.", "danger")
            return redirect(url_for("care.list_all_cares"))

        success, error = care_service.delete_care()
        if error:
            flash(error, "danger")
        else:
            flash("Soin supprimé avec succès.", "success")
        return redirect(url_for("care.list_all_cares"))








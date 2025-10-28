from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from app.forms.care_forms import CareCreateForm, CareUpdateForm
from app.services.care_service import CareService
from app.services.user_service import UserService
from app.utils.security import detect_sql_injection, sanitize_html
from datetime import datetime

class CareController:

    @classmethod
    def list_all_cares(cls):
        """Liste tous les rapports de soins"""
        try:
            cares = CareService.list_all_cares()
            return render_template("care/list_all_cares.html", cares=cares)
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la récupération des soins : {e}")
            flash("Erreur serveur lors de la récupération des soins.", "danger")
            return redirect(url_for("main.index"))

    @classmethod
    def get_care_by_id(cls, care_id):
        """Récupère un rapport de soin par son ID"""
        try:
            care = CareService.get_care_by_id(care_id)
            if not care:
                flash("Rapport de soin introuvable.", "warning")
            return care
        except Exception as e:
            current_app.logger.error(f"Erreur récupération soin : {e}")
            flash("Erreur serveur. Merci de réessayer plus tard.", "danger")
            return None

    @classmethod
    def list_all_vets(cls):
        """
        Retourne la liste de tous les vétérinaires.
        Utile pour les formulaires ou API.
        """
        try:
            vets = UserService.list_all_vets()
            return vets
        except Exception as e:
            current_app.logger.error(f"Erreur récupération vétérinaires : {e}")
            return []

    @staticmethod
    def create_care():
        """Création d'un rapport de soin"""
        form = CareCreateForm()
        if request.method == "POST":
            try:
                if form.validate_on_submit():
                    print("Animal ID sélectionné :", form.animal_id.data)
                    animal_id = form.animal_id.data
                    vet_id = form.vet_id.data
                    type_care = sanitize_html(form.type_care.data)
                    description = sanitize_html(form.description.data)
                    date_care = form.date_care.data or datetime.now()

                    # Vérification injection SQL simple
                    if detect_sql_injection(type_care) or detect_sql_injection(description):
                        flash("Entrée invalide détectée.", "danger")
                        return redirect(request.url)

                    care = CareService.create_care(
                        animal_id, vet_id, type_care, description, date_care
                    )
                    if care:
                        flash("Rapport de soin créé avec succès.", "success")
                        return redirect(url_for("care.list_all_cares"))
                    else:
                        flash("Impossible de créer le rapport de soin.", "danger")
            except Exception as e:
                current_app.logger.error(f"Erreur création soin : {e}")
                flash("Erreur serveur. Merci de réessayer plus tard.", "danger")

        return render_template("care/create_care.html", form=form)

    @staticmethod
    def update_care(care_id):
        """Modification d'un rapport de soin existant"""
        try:
            care = CareController.get_care_by_id(care_id)
            if not care:
                return redirect(url_for("care.list_all_cares"))

            form = CareUpdateForm(obj=care)
            if request.method == "POST":
                if form.validate_on_submit():
                    care.animal_id = form.animal_id.data
                    care.user_id = form.vet_id.data
                    care.type_care = sanitize_html(form.type_care.data)
                    care.description = sanitize_html(form.description.data)
                    care.date_care = form.date_care.data or care.date_care

                    updated = CareService.update_care(
                        care.id, care.animal_id, care.user_id, care.type_care, care.description, care.date_care
                    )
                    if updated:
                        flash("Rapport de soin mis à jour.", "success")
                        return redirect(url_for("care.list_all_cares"))
                    else:
                        flash("Impossible de mettre à jour le rapport de soin.", "danger")

            return render_template("care/update_care.html", form=form, care=care)

        except Exception as e:
            current_app.logger.error(f"Erreur modification soin : {e}")
            flash("Erreur serveur. Merci de réessayer plus tard.", "danger")
            return redirect(url_for("care.list_all_cares"))

    @staticmethod
    def delete_care(care_id):
        """Suppression d'un rapport de soin"""
        try:
            deleted = CareService.delete_care(care_id)
            if deleted:
                flash("Rapport de soin supprimé.", "success")
            else:
                flash("Impossible de supprimer le rapport de soin.", "warning")
        except Exception as e:
            current_app.logger.error(f"Erreur suppression soin : {e}")
            flash("Erreur serveur. Merci de réessayer plus tard.", "danger")

        return redirect(url_for("care.list_all_cares"))

    @staticmethod
    def api_list_all_cares():
        """Retourne les soins en JSON pour fetch/ajax"""
        try:
            cares = CareService.list_all_cares()
            cares_json = [care.__dict__ for care in cares]
            return jsonify({"success": True, "cares": cares_json})
        except Exception as e:
            current_app.logger.error(f"Erreur API soins : {e}")
            return jsonify({"success": False, "message": "Erreur serveur"}), 500




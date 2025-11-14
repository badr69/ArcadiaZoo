from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from app.forms.habitat_forms import HabitatCreateForm
from app.services.habitat_service import HabitatService


class HabitatController:
    """
    Controller pour gérer les routes liées aux habitats.
    Toutes les méthodes sont des classmethods pour rester cohérent avec l'OOP.
    """

    @classmethod
    def list_all_habitats(cls):
        """Afficher la liste de tous les habitats"""
        # TODO: ajouter pagination si nécessaire
        habitats = HabitatService.list_all_habitats()
        return render_template('habitat/list_all_habitats.html', habitats=habitats, current_user=current_user)

    @classmethod
    def show_habitat(cls, habitat_id):
        """Afficher un habitat spécifique"""
        habitat = HabitatService.get_habitat_by_id(habitat_id)
        if not habitat:
            flash("Habitat introuvable.", "warning")
            # TODO: gérer une page 404 spécifique
            return redirect(url_for('habitats.list_all_habitats'))
        return render_template('habitat/habitat_details.html', habitat=habitat, current_user=current_user)

    @classmethod
    def create_habitat(cls):
        form = HabitatCreateForm()
        """Créer un nouvel habitat via formulaire"""
        if request.method == 'POST':
            name = request.form.get('name')
            url_image = request.form.get('url_image')
            description = request.form.get('description')

            # TODO: valider les données (non vide, format URL, etc.)
            # TODO: vérifier que le nom n'existe pas déjà
            new_habitat = HabitatService.create_habitat(name, url_image, description)
            if new_habitat:
                flash("Habitat créé avec succès.", "success")
                return redirect(url_for('habitats.list_all_habitats'))
            else:
                flash("Erreur lors de la création de l'habitat.", "danger")

        return render_template('habitat/create_habitat.html', form=form, current_user=current_user)

    @classmethod
    def update_habitat(cls, habitat_id):
        """Mettre à jour un habitat existant via formulaire"""
        habitat = HabitatService.get_habitat_by_id(habitat_id)
        if not habitat:
            flash("Habitat introuvable.", "warning")
            return redirect(url_for('habitats.list_all_habitats'))

        if request.method == 'POST':
            name = request.form.get('name')
            url_image = request.form.get('url_image')
            description = request.form.get('description')

            # TODO: valider les données avant mise à jour
            # TODO: vérifier unicité du nom si modifié
            success = habitat.update_habitat(name, url_image, description)
            if success:
                flash("Habitat mis à jour avec succès.", "success")
            else:
                flash("Erreur lors de la mise à jour de l'habitat.", "danger")

            return redirect(url_for('habitats.list_all_habitats'))

        return render_template('habitat/update_habitat.html', habitat=habitat, current_user=current_user)

    @classmethod
    def delete_habitat(cls, habitat_id):
        """Supprimer un habitat"""
        habitat = HabitatService.get_habitat_by_id(habitat_id)
        if not habitat:
            flash("Habitat introuvable.", "warning")
            # TODO: gérer le cas où l'habitat est déjà supprimé
        else:
            # TODO: vérifier dépendances avant suppression (animaux liés)
            success = habitat.delete_habitat()
            if success:
                flash("Habitat supprimé avec succès.", "success")
            else:
                flash("Erreur lors de la suppression de l'habitat.", "danger")

        return redirect(url_for('habitats.list_all_habitats'))

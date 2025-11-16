from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from app.forms.habitat_forms import HabitatCreateForm, HabitatUpdateForm
from app.services.animal_service import AnimalService
from app.services.habitat_service import HabitatService
from app.services.imaage_service import ImageService
class HabitatController:

    @classmethod
    def create_habitat(cls):
        """Créer un nouvel habitat via formulaire sécurisé"""
        # TODO: gérer erreurs si ImageService ou AnimalService échouent
        images = ImageService.list_all_images()  # [(id, url_image), ...]

        image_choices = [(img[0], img[1]) for img in images]
        form = HabitatCreateForm(image_choices=image_choices)

        if form.validate_on_submit():
            # TODO: vérifier unicité du nom avant création
            name = form.name.data.strip()
            description = form.description.data.strip()
            image_id = form.image_id.data
            selected_animals = form.animals.data  # liste d'ids

            # TODO: vérifier que image_id existe dans la BDD
            # TODO: vérifier que selected_animals existe dans la BDD

            # TODO: utiliser un try/except pour attraper les erreurs SQL
            new_habitat = HabitatService.create_habitat(
                name=name,
                description=description,
                image_id=image_id,

            )

            if new_habitat:
                flash("Habitat créé avec succès.", "success")
                return redirect(url_for('habitats.list_all_habitats'))
            else:
                flash("Erreur lors de la création de l'habitat.", "danger")

        return render_template('habitat/create_habitat.html', form=form, current_user=current_user)

    @classmethod
    def update_habitat(cls, habitat_id):
        """Mettre à jour un habitat existant via formulaire sécurisé"""
        habitat = HabitatService.get_habitat_by_id(habitat_id)
        if not habitat:
            flash("Habitat introuvable.", "warning")
            return redirect(url_for('habitats.list_all_habitats'))

        images = ImageService.list_all_images()
        animals = AnimalService.list_all_animals()

        image_choices = [(img[0], img[1]) for img in images]
        animal_choices = [(a[0], a[1]) for a in animals]

        # TODO: vérifier que habitat.animals est bien une liste d'objets valides
        form = HabitatUpdateForm(
            image_choices=image_choices,
            name=habitat.name,
            description=habitat.description,
            animals=[a.id for a in habitat.animals],
            image_id=habitat.image_id
        )
        form.animals.choices = animal_choices

        if form.validate_on_submit():
            # TODO: vérifier unicité du nom si modifié
            # TODO: vérifier que image_id et animals existent toujours en BDD
            habitat.name = form.name.data.strip()
            habitat.description = form.description.data.strip()
            habitat.image_id = form.image_id.data
            selected_animals = form.animals.data

            # TODO: wrap dans try/except pour attraper erreurs SQL
            success = HabitatService.update_habitat(habitat, selected_animals)
            if success:
                flash("Habitat mis à jour avec succès.", "success")
            else:
                flash("Erreur lors de la mise à jour de l'habitat.", "danger")

            return redirect(url_for('habitats.list_all_habitats'))

        return render_template('habitat/update_habitat.html', form=form, habitat=habitat, current_user=current_user)

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
    def delete_habitat(cls, habitat_id):
        """Supprimer un habitat"""
        habitat = HabitatService.get_habitat_by_id(habitat_id)
        if not habitat:
            flash("Habitat introuvable.", "warning")
            # TODO: gérer le cas où l'habitat est déjà supprimé
        else:
            # TODO: vérifier dépendances avant suppression (animaux liés)
            # TODO: wrap dans try/except pour attraper erreurs SQL
            success = habitat.delete_habitat()
            if success:
                flash("Habitat supprimé avec succès.", "success")
            else:
                flash("Erreur lors de la suppression de l'habitat.", "danger")

        return redirect(url_for('habitats.list_all_habitats'))





# from flask import render_template, request, redirect, url_for, flash
# from flask_login import current_user
# from app.forms.habitat_forms import HabitatCreateForm
# from app.services.habitat_service import HabitatService
#
#
# class HabitatController:
#     """
#     Controller pour gérer les routes liées aux habitats.
#     Toutes les méthodes sont des classmethods pour rester cohérent avec l'OOP.
#     """
#
#     @classmethod
#     def list_all_habitats(cls):
#         """Afficher la liste de tous les habitats"""
#         # TODO: ajouter pagination si nécessaire
#         habitats = HabitatService.list_all_habitats()
#         return render_template('habitat/list_all_habitats.html', habitats=habitats, current_user=current_user)
#
#     @classmethod
#     def show_habitat(cls, habitat_id):
#         """Afficher un habitat spécifique"""
#         habitat = HabitatService.get_habitat_by_id(habitat_id)
#         if not habitat:
#             flash("Habitat introuvable.", "warning")
#             # TODO: gérer une page 404 spécifique
#             return redirect(url_for('habitats.list_all_habitats'))
#         return render_template('habitat/habitat_details.html', habitat=habitat, current_user=current_user)
#
#     @classmethod
#     def create_habitat(cls):
#         form = HabitatCreateForm()
#         """Créer un nouvel habitat via formulaire"""
#         if request.method == 'POST':
#             name = request.form.get('name')
#             url_image = request.form.get('url_image')
#             description = request.form.get('description')
#
#             # TODO: valider les données (non vide, format URL, etc.)
#             # TODO: vérifier que le nom n'existe pas déjà
#             new_habitat = HabitatService.create_habitat(name, url_image, description)
#             if new_habitat:
#                 flash("Habitat créé avec succès.", "success")
#                 return redirect(url_for('habitats.list_all_habitats'))
#             else:
#                 flash("Erreur lors de la création de l'habitat.", "danger")
#
#         return render_template('habitat/create_habitat.html', form=form, current_user=current_user)
#
#     @classmethod
#     def update_habitat(cls, habitat_id):
#         """Mettre à jour un habitat existant via formulaire"""
#         habitat = HabitatService.get_habitat_by_id(habitat_id)
#         if not habitat:
#             flash("Habitat introuvable.", "warning")
#             return redirect(url_for('habitats.list_all_habitats'))
#
#         if request.method == 'POST':
#             name = request.form.get('name')
#             url_image = request.form.get('url_image')
#             description = request.form.get('description')
#
#             # TODO: valider les données avant mise à jour
#             # TODO: vérifier unicité du nom si modifié
#             success = habitat.update_habitat(name, url_image, description)
#             if success:
#                 flash("Habitat mis à jour avec succès.", "success")
#             else:
#                 flash("Erreur lors de la mise à jour de l'habitat.", "danger")
#
#             return redirect(url_for('habitats.list_all_habitats'))
#
#         return render_template('habitat/update_habitat.html', habitat=habitat, current_user=current_user)
#
#     @classmethod
#     def delete_habitat(cls, habitat_id):
#         """Supprimer un habitat"""
#         habitat = HabitatService.get_habitat_by_id(habitat_id)
#         if not habitat:
#             flash("Habitat introuvable.", "warning")
#             # TODO: gérer le cas où l'habitat est déjà supprimé
#         else:
#             # TODO: vérifier dépendances avant suppression (animaux liés)
#             success = habitat.delete_habitat()
#             if success:
#                 flash("Habitat supprimé avec succès.", "success")
#             else:
#                 flash("Erreur lors de la suppression de l'habitat.", "danger")
#
#         return redirect(url_for('habitats.list_all_habitats'))

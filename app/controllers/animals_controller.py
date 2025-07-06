from flask import render_template, request, redirect, url_for, flash
from app.services.animal_service import AnimalService

from app.forms import AnimalCreateForm


def list_animals():
    animals = AnimalService.get_all_animals()
    return render_template('animals/index.html', animals=animals)

def create_animal():
    form = AnimalCreateForm()
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        success = AnimalService.create_animal(name, species)
        if success:
            flash("Animal ajouté avec succès.", "success")
        else:
            flash("Erreur lors de l'ajout de l'animal.", "danger")
        return redirect(url_for('animal_bp.list_animals'))
    return render_template('animals/create.html', form=form)

def edit_animal(animal_id):
    animal = AnimalService.get_animal_by_id(animal_id)
    if not animal:
        flash("Animal introuvable.", "warning")
        return redirect(url_for('animal_bp.list_animals'))
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        success = AnimalService.update_animal(animal_id, name, species)
        if success:
            flash("Animal modifié avec succès.", "success")
        else:
            flash("Erreur lors de la modification.", "danger")
        return redirect(url_for('animal_bp.list_animals'))
    return render_template('animals/edit.html', animal=animal)

def delete_animal(animal_id):
    success = AnimalService.delete_animal(animal_id)
    if success:
        flash("Animal supprimé.", "success")
    else:
        flash("Erreur lors de la suppression.", "danger")
    return redirect(url_for('animal_bp.list_animals'))

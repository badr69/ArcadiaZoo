from flask import render_template, redirect, url_for, flash
from app.forms.food_forms import FoodCreateForm, FoodUpdateForm
from app.services.food_service import FoodService


class FoodController:

    # ======================================================
    # STATIC METHODS (CREATE & LIST)
    # ======================================================
    @staticmethod
    def list_all_foods():
        foods = FoodService.list_all_foods()
        return render_template("food/list_all_foods.html", foods=foods)

    @staticmethod
    def create_food():
        form = FoodCreateForm()

        if form.validate_on_submit():
            try:
                FoodService.create_food(
                    animal_id=form.animal_id.data,
                    vet_id=form.vet_id.data,
                    employee_id=form.employee_id.data,
                    name_food=form.name_food.data,
                    quantity=form.quantity.data,
                    date_food=form.date_food.data
                )
                flash("Food créé avec succès.", "success")
                return redirect(url_for("food.list_all_foods"))
            except ValueError as e:
                flash(str(e), "danger")

        return render_template("food/create_food.html", form=form)

    # ======================================================
    # INSTANCE METHODS (GET, UPDATE, DELETE)
    # ======================================================
    def __init__(self, food_id):
        try:
            self.service = FoodService(food_id)
        except ValueError:
            self.service = None

    def get_food_by_id(self):
        if not self.service:
            flash("Food non trouvé.", "danger")
            return redirect(url_for("food.list_all_foods"))

        food = self.service.get_food_by_id()
        return render_template("food/food_details.html", food=food)

    def update_food(self):
        if not self.service:
            flash("Food non trouvé.", "danger")
            return redirect(url_for("food.list_all_foods"))

        food = self.service.get_food_by_id()

        # Pré-remplissage du formulaire
        form = FoodUpdateForm(
            animal_id=food.animal_id,
            vet_id=food.vet_id,
            employee_id=food.employee_id,
            name_food=food.name_food,
            quantity=food.quantity,
            date_food=food.date_food
        )

        if form.validate_on_submit():
            try:
                self.service.update_food(
                    animal_id=form.animal_id.data,
                    vet_id=form.vet_id.data,
                    employee_id=form.employee_id.data,
                    name_food=form.name_food.data,
                    quantity=form.quantity.data,
                    date_food=form.date_food.data
                )
                flash("Food mis à jour avec succès.", "success")
                return redirect(url_for("food.list_all_foods"))
            except ValueError as e:
                flash(str(e), "danger")

        return render_template("food/update_food.html", form=form, food=food)

    def delete_food(self):
        if not self.service:
            flash("Food non trouvé.", "danger")
        else:
            deleted = self.service.delete_food()
            if deleted:
                flash("Food supprimé avec succès.", "success")
            else:
                flash("Erreur lors de la suppression.", "danger")
        return redirect(url_for("food.list_all_foods"))

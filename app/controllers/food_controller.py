from flask import render_template, request, redirect, url_for, flash
from app.forms.food_forms import FoodForm
from app.models.animal_model import AnimalModel
from app.services.food_service import FoodService
from app.models.food_model import FoodModel

class FoodController:

    @staticmethod
    def list_all_animals():
        animals = AnimalModel.list_all_animals()
        return render_template("animal/list_all_animals.html", animals=animals)

    @staticmethod
    def list_all_foods():
        foods = FoodService.list_all_foods()
        return render_template("food/list_all_foods.html", foods=foods)

    @staticmethod
    def get_food_by_id(food_id):
        food = FoodService.get_food_by_id(food_id)
        if food is None:
            flash("Food not found.", "danger")
            return redirect(url_for('food.list_all_foods'))
        return render_template("food/detail_food.html", food=food)

    @staticmethod
    def create_food():
        form = FoodForm()
        animals = FoodService.list_all_animals()
        form.animal.choices = [(a.id, a.name) for a in animals]

        if form.validate_on_submit():
            feeding = FoodModel(
                animal_id=form.animal.data,
                type_food=form.type_food.data,
                quantity=form.quantity.data,
                date_food=form.date_food.data
            )
            result = FoodService.create_food(feeding)
            if result["status"]:
                flash("Food entry created successfully.", "success")
                return redirect(url_for("food.list_all_foods"))
            else:
                flash("Error creating food entry.", "danger")

        return render_template("food/create_food.html", form=form)

    @staticmethod
    def update_food(food_id):
        print("food_id reçu :", food_id)

        food = FoodService.get_food_by_id(food_id)
        if not food:
            flash("Food entry not found.", "danger")
            return redirect(url_for("food.list_all_foods"))

        form = FoodForm()
        animals = FoodService.list_all_animals()
        form.animal.choices = [(a.id, a.name) for a in animals]

        # Pré-remplir le formulaire (GET uniquement)
        if request.method == "GET":
            form.animal.data = food.animal_id
            form.type_food.data = food.type_food
            form.quantity.data = float(food.quantity)
            form.date_food.data = food.date_food

        if form.validate_on_submit():
            updated_food = FoodModel(
                id=food_id,
                animal_id=form.animal.data,
                type_food=form.type_food.data,
                quantity=form.quantity.data,
                date_food=form.date_food.data
            )
            result = FoodService.update_food(updated_food)
            if result["status"]:
                flash("Food entry updated successfully.", "success")
                return redirect(url_for("food.list_all_foods"))
            else:
                flash("Error updating food entry.", "danger")

        return render_template("food/update_food.html", form=form, food_id=food_id)

    @staticmethod
    def delete_food(food_id):
        result = FoodService.delete_food(food_id)
        if result["status"]:
            flash("Food entry deleted successfully.", "success")
        else:
            flash("Error deleting food entry.", "danger")
        return redirect(url_for("food.list_all_foods"))

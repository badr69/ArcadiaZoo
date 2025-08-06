# TODO: Importation des dépendances
from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.contact_forms import ContactForm
from app.forms.auth_forms import LoginForm
from app.forms.review_form import ReviewForm
from app.models.habitat_model import Habitat
from app.models.service_model import ServiceModel
from app.models.animal_model import AnimalModel
from app.controllers.review_controller import ReviewController
from app.utils.decorators import roles_required


main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = ReviewForm()
    animals = AnimalModel.list_all_animals()
    habitats = Habitat.list_all_habitats()
    services = ServiceModel.list_all_services()

    if form.validate_on_submit():
        # Créer un review avec les données du formulaire
        review = Review(
            pseudo=form.pseudo.data,
            message=form.message.data,
            rating=form.rating.data,
            element_id="global"
        )
        review.save()
        flash("Merci pour votre avis !", "success")
        return redirect(url_for('main.index'))

    # Charger les reviews
    reviews_data = ReviewController.get_review_by_element_id("global")
    return render_template(
        "index.html",
                           form=form,
                           animals=animals,
                           habitats=habitats,
                           services=services,
                           reviews=reviews_data
                           )

@main_bp.route('/services/')
def services():
    services_objects = ServiceModel.list_all_services()  # renvoie une liste d'objets Habitat
    services = []
    for s in services_objects:
        services.append({
            'id': s.id,
            'name': s.name,
            'url_image': s.url_image,
            'description': s.description,
            'created_at': s.created_at,
            'updated_at': s.updated_at
        })
    return render_template('services.html', services=services)


@main_bp.route('/animals/')
def animals():
    animals_objects = AnimalModel.list_all_animals()  # ta méthode qui récupère les animaux
    animals = []
    for a in animals_objects:
        animals.append({
            'id': a.id,
            'name': a.name,
            'url_image': a.url_image,# chemin relatif depuis static
            'description': a.description,
            'created_at': a.created_at,
            'updated_at': a.updated_at
            # autres champs si besoin
        })
    return render_template('animals.html', animals=animals)

@main_bp.route('/habitats/')
def habitats():
    habitats_objects = Habitat.list_all_habitats()  # renvoie une liste d'objets Habitat
    habitats = []
    for h in habitats_objects:
        habitats.append({
            'id': h.id,
            'name': h.name,
            'url_image': h.url_image,
            'description': h.description,
            'created_at': h.created_at,
            'updated_at': h.updated_at
        })
    return render_template('habitats.html', habitats=habitats)

@main_bp.route("/contact")
def contact():
    form = ContactForm()
    return render_template("contact.html", form=form)

@main_bp.route("/login")
def login():
    form = LoginForm()
    return render_template("auth/login.html", form=form)

@main_bp.route("/admin_dash")
@roles_required("admin")
def admin_dash():
    return render_template("dash/admin_dash.html")

@main_bp.route('/employee_dash', methods=['GET', 'POST'])
@roles_required("admin", "employee")
def employee_dash():
     return render_template("dash/employee_dash.html")

@main_bp.route('/vet_dash', methods=['GET', 'POST'])
@roles_required("admin", "vet")
def vet_dash():
    return render_template("dash/vet_dash.html")

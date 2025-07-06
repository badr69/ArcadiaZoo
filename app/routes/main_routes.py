# app/routes/main_routes.py
from flask import Blueprint, render_template
from app.forms import ContactForm, LoginForm, ReviewForm

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    form = ReviewForm()
    return render_template('index.html', form=form)

@main_bp.route('/services')
def services():
    return render_template('services.html')

@main_bp.route('/animals/')
def animals():
    return render_template('animals.html')

@main_bp.route('/habitats/')
def habitats():
    return render_template('habitats.html')

# @main_bp.route('/contact')
# def contact():
#     return render_template('contact.html')


 # Assure-toi que ce chemin est correct

@main_bp.route("/contact")
def contact():
    form = ContactForm()
    return render_template("contact.html", form=form)

@main_bp.route("/login")
def login():
    form = LoginForm()
    return render_template("auth/login.html", form=form)

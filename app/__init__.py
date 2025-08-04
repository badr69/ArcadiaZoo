import os
from flask import Flask
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from app.models.user_model import UserModel
from app.extensions.login_manager import login_manager


csrf = CSRFProtect()

def create_app():
    load_dotenv()  # Charge les variables depuis .env

    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change_me')  # Bonne pratique

    upload_folder = os.path.join('app', 'static', 'uploads')
    app.config['upload_folder'] = upload_folder

    app.config['ANIMAL_IMG_FOLDER'] = os.path.join(upload_folder, 'animal_img')
    app.config['HABITAT_IMG_FOLDER'] = os.path.join(upload_folder, 'habitat_img')
    app.config['SERVICE_IMG_FOLDER'] = os.path.join(upload_folder, 'service_img')
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 30 MB max
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    csrf.init_app(app)  # Protection CSRF via Flask-WTF

    login_manager.init_app(app)  # Init login manager **après** la création de l'app
    login_manager.login_view = 'auth.login'  # nom de ta route de login

    # Enregistrement des blueprints
    from app.routes.role_routes import role_bp
    app.register_blueprint(role_bp)

    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    from app.routes.admin_route import admin_bp
    app.register_blueprint(admin_bp)

    from app.routes.employee_route import employee_bp
    app.register_blueprint(employee_bp)
    from app.routes.vet_route import vet_bp

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    from app.routes.habitats_routes import habitat_bp
    app.register_blueprint(habitat_bp)

    from app.routes.img_habitat_route import img_habitat_bp
    app.register_blueprint(img_habitat_bp)

    from app.routes.animal_routes import animal_bp
    app.register_blueprint(animal_bp)

    from app.routes.service_routes import service_bp
    app.register_blueprint(service_bp)

    from app.routes.review_route import reviews_bp
    app.register_blueprint(reviews_bp)

    return app


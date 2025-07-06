import os
from flask import Flask
from dotenv import load_dotenv
from flask_wtf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    load_dotenv()  # Charge les variables depuis .env

    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change_me')  # Bonne pratique

    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB max
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    csrf.init_app(app)  # Protection CSRF via Flask-WTF

    from app.routes.user_routes import user_bp

    app.register_blueprint(user_bp)# Enregistrement d'un blueprint utilisateur

    from app.routes.admin_route import admin_bp
    app.register_blueprint(admin_bp)

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    from app.routes.habitats_routes import habitat_bp
    app.register_blueprint(habitat_bp)


    return app





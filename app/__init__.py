from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY

    return app

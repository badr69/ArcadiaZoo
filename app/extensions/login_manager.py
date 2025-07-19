from flask_login import LoginManager
from app.models.user_model import UserModel

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get_user_by_id(int(user_id))





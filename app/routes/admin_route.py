# Exemple dans app/routes/admin_routes.py
from flask import Blueprint, render_template
from app.services.user_service import UserService

admin_bp = Blueprint('admin', __name__, url_prefix="/admin")

@admin_bp.route('/admin_dash')
def admin_dash():
    return render_template('dash/admin_dash.html')


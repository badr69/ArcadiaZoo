from flask import Blueprint, render_template
from app.forms.auth_forms import LogoutForm
#

employee_bp = Blueprint('employee', __name__, url_prefix="/employee")

@employee_bp.route('/employee_dash')
def employee_dash():
    form = LogoutForm()
    return render_template('dash/employee_dash.html', form=form)
#
# from flask import Blueprint, render_template
# from app.forms.auth_forms import LogoutForm
# from app.models.review_model import Review  # Assure-toi que ce fichier existe et contient une méthode get_all()
#
# employee_bp = Blueprint('employee', __name__, url_prefix="/employee")
# #
# # @employee_bp.route('/employee_dash')
# # def employee_dash():
# #     form = LogoutForm()
# #     reviews = Review.get_all()  # Méthode à créer si elle n’existe pas encore
# #     return render_template('dash/employee_dash.html', form=form, reviews=reviews)
# # from app.models.review import Review
# # #
# # @employee_bp.route('/employee_dash')
# # def employee_dash():
# #     form = LogoutForm()
# #     reviews = Review.get_all()
# #     return render_template('dash/employee_dash.html', form=form, reviews=reviews)
# @employee_bp.route('/employee_dash')
# def employee_dash():
#     form = ReviewForm()
#     reviews = Review.get_all()
#     return render_template('dash/employee_dash.html', form=form,  reviews=reviews)
#
#
# # @main_bp.route('/employee_dash')
# # def employee_dash():
# #     reviews_data = Review.get_by_element_id("global")  # ou autre filtre
# #     return render_template("dash/employee_dash.html", reviews=reviews_data)

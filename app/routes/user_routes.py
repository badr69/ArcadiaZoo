from flask import Blueprint, render_template, flash, request, abort, redirect, url_for
from app.controllers.user_controller import UserController
from app.forms import UpdateUserForm

user_bp = Blueprint('user', __name__, url_prefix="/user")


@user_bp.route('/create_user', methods=['GET', 'POST'])
def create_user():
    return UserController.create_user()

@user_bp.route('/list_all_users')
def list_all_users():
    users = UserController.get_all_users()
    return render_template('user/list_all_users.html', users=users)


@user_bp.route('/user/<int:user_id>')
def get_user_by_id(user_id):
    user = UserController.get_user_by_id(user_id)
    if user is None:
        abort(404)
    return render_template("user/user_detail.html", user=user)



@user_bp.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    user = UserController.get_user_by_id(user_id)
    # user = User.query.get_or_404(user_id)  # ou ta méthode d'accès
    form = UpdateUserForm()  # pré-remplit le formulaire avec les données existantes

    if form.validate_on_submit():
        # met à jour l'utilisateur avec les données du formulaire
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role_name.data
        # commit en base
        flash('Utilisateur mis à jour avec succès', 'success')
        return redirect(url_for('user.get_user_by_id', user_id=user.id))
    # si GET ou erreur de validation, affiche le formulaire
    return render_template('user/update_user.html', form=form, user=user)

@user_bp.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    success = UserController.delete_user(user_id)
    if success:
        flash("Utilisateur supprimé avec succès", "success")
    else:
        flash("Erreur lors de la suppression de l'utilisateur", "danger")
    return redirect(url_for('user.list_all_users'))


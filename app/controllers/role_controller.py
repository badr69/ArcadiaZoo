# app/controllers/role_controller.py

from flask import render_template, redirect, url_for, flash
from app.forms.role_forms import CreateRoleForm, UpdateRoleForm
from app.services.role_service import RoleService
from app.utils.security import sanitize_html


class RoleController:

    # ======================================================
    # LIST ALL ROLES
    # ======================================================
    @staticmethod
    def list_all_roles():
        roles = RoleService.list_all_roles()   # -> liste de RoleService
        return render_template("role/list_all_roles.html", roles=roles)

    # ======================================================
    # GET ROLE BY ID
    # ======================================================
    @staticmethod
    def get_role_by_id(role_id):
        role_service, error = RoleService.get_role_by_id(role_id)
        if error:
            flash(error, "danger")
            return redirect(url_for("role.list_all_roles"))

        # Passer l'objet RoleService au template
        return render_template("role/role_details.html", role=role_service)

    # ======================================================
    # CREATE ROLE
    # ======================================================
    @staticmethod
    def create_role():
        form = CreateRoleForm()
        if form.validate_on_submit():
            name = sanitize_html(form.name.data)

            role_service, error = RoleService.create_role(name)
            if error:
                flash(error, "danger")
            else:
                flash("Rôle créé avec succès.", "success")
                return redirect(url_for("role.list_all_roles"))

        return render_template("role/create_role.html", form=form)

    # ======================================================
    # CONTROLLER AVEC INSTANCE
    # ======================================================
    def __init__(self, role_id):
        self.role_service, self.error = RoleService.get_role_by_id(role_id)

    # ======================================================
    # UPDATE
    # ======================================================
    def update_role(self):
        if not self.role_service:
            flash(self.error, "danger")
            return redirect(url_for("role.list_all_roles"))

        # Pré-remplit le formulaire avec un RoleService
        form = UpdateRoleForm(obj=self.role_service)

        if form.validate_on_submit():
            name = sanitize_html(form.name.data)

            success, error = self.role_service.update_role(name)
            if success:
                flash("Rôle mis à jour avec succès.", "success")
                return redirect(url_for("role.list_all_roles"))
            else:
                flash(error, "danger")

        return render_template(
            "role/update_role.html",
            form=form,
            role=self.role_service
        )

    # ======================================================
    # DELETE
    # ======================================================
    def delete_role(self):
        if not self.role_service:
            flash(self.error, "danger")
            return redirect(url_for("role.list_all_roles"))

        success, error = self.role_service.delete_role()

        if success:
            flash("Rôle supprimé avec succès.", "success")
        else:
            flash(error, "danger")

        return redirect(url_for("role.list_all_roles"))










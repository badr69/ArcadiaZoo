from flask import render_template, redirect, url_for, flash, request
from app.services.role_service import RoleService
from app.utils.security import sanitize_html, detect_sql_injection
from app.forms.role_forms import CreateRoleForm, DeleteRoleForm, UpdateRoleForm


class RoleController:
    def __init__(self):
        self.role_service = RoleService()

    # ===================== CREATE =====================

    def create_role(self):
        form = CreateRoleForm()

        if form.validate_on_submit():
            name = sanitize_html(form.name.data)

            if detect_sql_injection(name):
                flash("Entrée invalide détectée.", "danger")
                return render_template("role/create_role.html", form=form)

            role, message = self.role_service.create_role(name)
            if role:
                flash(message, "success")
                return redirect(url_for("role.list_all_roles"))
            else:
                flash(message, "danger")

        return render_template("role/create_role.html", form=form)

    # ===================== UPDATE =====================

    def update_role(self, role_id):
        role = self.role_service.get_role_by_id(role_id)
        if not role:
            flash("Rôle introuvable", "danger")
            return redirect(url_for("role.list_all_roles"))

        # Préremplir le formulaire avec la valeur actuelle
        form = UpdateRoleForm(obj=role)

        if form.validate_on_submit():
            name = sanitize_html(form.name.data)

            if detect_sql_injection(name):
                flash("Entrée invalide détectée.", "danger")
                return render_template("role/update_role.html", form=form, role=role)

            result, status = self.role_service.update_role(role, name)
            if status == 200:
                flash(result.get("message"), "success")
                return redirect(url_for("role.list_all_roles"))
            else:
                flash(result.get("error"), "danger")

        return render_template("role/update_role.html", form=form, role=role)

    # ===================== DELETE =====================


    def delete_role(self, role_id):
        role = self.role_service.get_role_by_id(role_id)
        if not role:
            flash("Rôle introuvable", "danger")
            return redirect(url_for("role.list_all_roles"))

        form = DeleteRoleForm()

        if form.validate_on_submit():
            success = self.role_service.delete_role(role)
            if success:
                flash("Rôle supprimé avec succès", "success")
            else:
                flash("Erreur lors de la suppression du rôle", "danger")
            return redirect(url_for("role.list_all_roles"))

        # On affiche d'abord la page de confirmation
        return render_template("role/delete_role.html", form=form, role=role)

    # ===================== READ =====================
    @classmethod
    def list_all_roles(cls):
        roles = RoleService().list_all_roles()
        return render_template("role/list_all_roles.html", roles=roles)

    @classmethod
    def get_role_by_id(cls, role_id):
        role = RoleService().get_role_by_id(role_id)
        if not role:
            flash("Rôle introuvable", "danger")
            return redirect(url_for("role.list_all_roles"))
        return render_template("role/role_detail.html", role=role)

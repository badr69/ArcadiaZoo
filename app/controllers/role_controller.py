from app.forms.role_forms import CreateRoleForm, UpdateRoleForm
from app.services.role_service import RoleService
from flask import render_template, url_for, redirect, flash, request
from app.utils.security import sanitize_html, detect_sql_injection


class RoleController:

    @staticmethod
    def list_all_roles():
        roles = RoleService.list_all_roles()  # Role avec created_at et updated_at
        return render_template("role/list_all_roles.html", roles=roles)

    @staticmethod
    def get_role_by_id(role_id):
        role = RoleService.get_role_by_id(role_id)
        if not role:
            flash("Rôle non trouvé", "warning")
            return redirect(url_for("role.list_all_roles"))
        return render_template("role/role_detail.html", role=role)

    @staticmethod
    def create_role():
        form = CreateRoleForm()
        if form.validate_on_submit():
            name = sanitize_html(form.name.data)

            if detect_sql_injection(name):
                flash("Entrée invalide détectée.", "danger")
                return render_template("role/create_role.html", form=form)

            success = RoleService.create_role(name)
            if success:
                flash("Rôle créé avec succès", "success")
                return redirect(url_for("role.list_all_roles"))
            else:
                flash("Erreur lors de la création du rôle", "danger")

        return render_template("role/create_role.html", form=form)

    @staticmethod
    def update_role(role_id):
        role = RoleService.get_role_by_id(role_id)
        if not role:
            flash("Rôle non trouvé", "warning")
            return redirect(url_for("role.list_all_roles"))

        form = UpdateRoleForm(obj=role)
        if form.validate_on_submit():
            name = sanitize_html(form.name.data)

            if detect_sql_injection(name):
                flash("Entrée invalide détectée.", "danger")
                return render_template("role/update_role.html", form=form, role=role)

            success = RoleService.update_role(role_id, name)
            if success:
                flash("Rôle mis à jour avec succès", "success")
                return redirect(url_for("role.list_all_roles"))
            else:
                flash("Erreur lors de la mise à jour du rôle", "danger")

        return render_template("role/update_role.html", form=form, role=role)

    @staticmethod
    def delete_role(role_id):
        role = RoleService.get_role_by_id(role_id)
        if not role:
            flash("Rôle non trouvé", "warning")
            return redirect(url_for("role.list_all_roles"))

        success = RoleService.delete_role(role_id)
        if success:
            flash("Rôle supprimé avec succès", "success")
        else:
            flash("Erreur lors de la suppression du rôle", "danger")

        return redirect(url_for("role.list_all_roles"))

from flask import render_template, url_for, redirect, flash
from app.forms.role_forms import CreateRoleForm, UpdateRoleForm
from app.services.role_service import RoleService
from app.utils.security import sanitize_html, detect_sql_injection

class RoleController:

    @staticmethod
    def list_all_roles():
        roles = RoleService.list_all_roles()  # liste de RoleModel
        return render_template("role/list_all_roles.html", roles=roles)

    @staticmethod
    def get_role_by_id(role_id):
        """Affiche un rôle par ID"""
        role = RoleService.get_role_by_id(role_id)
        print("DEBUG role:", role)
        if not role:
            flash("Rôle non trouvé", "warning")
            return redirect(url_for("role.list_all_roles"))
        return render_template("role/role_detail.html", role=role)

    @staticmethod
    def create_role():
        """Crée un rôle via formulaire"""
        form = CreateRoleForm()
        if form.validate_on_submit():
            name = sanitize_html(form.name.data)
            if detect_sql_injection(name):
                flash("Entrée invalide détectée.", "danger")
                return render_template("role/create_role.html", form=form)

            role = RoleService.create_role(name)
            if role:
                flash(f"Rôle '{role.name}' créé avec succès", "success")
                return redirect(url_for("role.list_all_roles"))
            else:
                flash("Erreur lors de la création du rôle", "danger")

        return render_template("role/create_role.html", form=form)

    @staticmethod
    def update_role(role_id):
        """Met à jour un rôle existant"""
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

            updated_role = RoleService.update_role(role, name)
            if updated_role:
                flash(f"Rôle '{updated_role.name}' mis à jour avec succès", "success")
                return redirect(url_for("role.list_all_roles"))
            else:
                flash("Erreur lors de la mise à jour du rôle", "danger")

        return render_template("role/update_role.html", form=form, role=role)

    @staticmethod
    def delete_role(role_id):
        """Supprime un rôle"""
        role = RoleService.get_role_by_id(role_id)
        if not role:
            flash("Rôle non trouvé", "warning")
            return redirect(url_for("role.list_all_roles"))

        success = RoleService.delete_role(role)
        if success:
            flash(f"Rôle '{role.name}' supprimé avec succès", "success")
        else:
            flash("Erreur lors de la suppression du rôle", "danger")

        return redirect(url_for("role.list_all_roles"))

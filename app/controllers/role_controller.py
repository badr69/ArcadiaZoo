from app.forms.role_forms import CreateRoleForm
from app.services.role_service import RoleService
from flask import render_template, url_for, redirect, flash
from app.utils.security import sanitize_html, detect_sql_injection


class RoleController:
    @staticmethod
    def list_all_roles():
        roles = RoleService.list_all_roles()
        return render_template("role/list_all_roles.html", roles=roles)

    @staticmethod
    def create_role():
        form = CreateRoleForm()
        if form.validate_on_submit():
            name = sanitize_html(form.name.data)

            # Vérification SQL Injection
            if detect_sql_injection(name):
                flash("Entrée invalide détectée.", "danger")
                return render_template("role/create_role.html", form=form)

            success = RoleService.create_role()
            if success:
                flash("User created with succcess", "success")
                return redirect(url_for("role.list_all_roles"))
            else:
                flash("Error when creating Role", "danger")

        return render_template("role/create_role.html", form=form)


from app.db.psql import get_db_connection

class RoleModel:
    """Classe représentant un rôle."""

    def __init__(self, role_id, name, created_at=None, updated_at=None):
        self.role_id = role_id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<RoleModel role_id={self.role_id} name={self.name}>"

    @classmethod
    def list_all_roles(cls):
        """Retourne une liste de tous les rôles sous forme d'objets RoleModel."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT role_id, name, created_at, updated_at FROM roles")
                    rows = cur.fetchall()
                    roles = [
                        cls(role_id=row[0], name=row[1], created_at=row[2], updated_at=row[3])
                        for row in rows
                    ]
                    return roles
        except Exception as e:
            print(f"[list_all_roles error]: {e}")
            return []

    @classmethod
    def get_role_by_id(cls, role_id: int):
        """Retourne un objet RoleModel pour un role_id donné, ou None si introuvable."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT role_id, name, created_at, updated_at FROM roles WHERE role_id = %s",
                        (role_id,)
                    )
                    row = cur.fetchone()
                    if row:
                        return cls(role_id=row[0], name=row[1], created_at=row[2], updated_at=row[3])
                    return None
        except Exception as e:
            print(f"[get_role_by_id error]: {e}")
            return None

    @classmethod
    def create_role(cls, name: str):
        """Crée un nouveau rôle et retourne l'objet RoleModel créé."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO roles (name) VALUES (%s) RETURNING role_id, name, created_at, updated_at",
                        (name,)
                    )
                    row = cur.fetchone()
                    conn.commit()
                    if row:
                        return cls(role_id=row[0], name=row[1], created_at=row[2], updated_at=row[3])
                    return None
        except Exception as e:
            print(f"[create_role error]: {e}")
            return None

    def update_role(self, name: str):
        """Met à jour le nom du rôle actuel et retourne l'objet RoleModel mis à jour."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE roles SET name = %s, updated_at = CURRENT_TIMESTAMP "
                        "WHERE role_id = %s RETURNING role_id, name, created_at, updated_at",
                        (name, self.role_id)
                    )
                    row = cur.fetchone()
                    conn.commit()
                    if row:
                        self.name = row[1]
                        self.updated_at = row[3]
                        return self
                    return None
        except Exception as e:
            print(f"[update_role error]: {e}")
            return None

    def delete_role(self):
        """Supprime le rôle actuel et retourne True si succès, False sinon."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "DELETE FROM roles WHERE role_id = %s",
                        (self.role_id,)
                    )
                    conn.commit()
                    return True
        except Exception as e:
            print(f"[delete_role error]: {e}")
            return False









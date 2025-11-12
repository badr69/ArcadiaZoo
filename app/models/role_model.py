# app/models/role_model.py
from app.db.psql import get_db_connection

class RoleModel:
    """Modèle représentant un rôle dans l'application."""

    def __init__(self, role_id=None, name=None, created_at=None, updated_at=None):
        self.role_id = role_id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def id(self):
        return self.role_id

    # ===================== CREATE =====================
    @classmethod
    def create_role(cls, name):
        """Crée un nouveau rôle et le retourne."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO roles (name)
                        VALUES (%s)
                        RETURNING role_id, name, created_at, updated_at
                    """, (name,))
                    row = cur.fetchone()
                    conn.commit()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"[create_role error]: {e}")
            return None

    # ===================== READ =====================
    @classmethod
    def get_role_by_id(cls, role_id):
        """Récupère un rôle par son ID."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT role_id, name, created_at, updated_at
                        FROM roles
                        WHERE role_id = %s
                    """, (role_id,))
                    row = cur.fetchone()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"[get_role_by_id error]: {e}")
            return None

    @classmethod
    def list_all_roles(cls):
        """Retourne tous les rôles existants."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT role_id, name, created_at, updated_at
                        FROM roles
                        ORDER BY name 
                    """)
                    rows = cur.fetchall()
                    return [cls(*row) for row in rows]
        except Exception as e:
            print(f"[list_all_roles error]: {e}")
            return []

    # ===================== UPDATE =====================
    def update_role(self, name):
        """Met à jour le nom d’un rôle."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE roles
                        SET name = %s, updated_at = NOW()
                        WHERE role_id = %s
                        RETURNING role_id, name, created_at, updated_at
                    """, (name, self.role_id))
                    row = cur.fetchone()
                    conn.commit()
                    if row:
                        self.name = row[1]
                        self.updated_at = row[3]
                        return {"message": "Rôle mis à jour."}, 200
                    else:
                        return {"error": "Rôle introuvable."}, 404
        except Exception as e:
            print(f"[update_role error]: {e}")
            return {"error": "Erreur serveur."}, 500

    # ===================== DELETE =====================
    def delete_role(self):
        """Supprime un rôle."""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM roles WHERE role_id = %s", (self.role_id,))
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"[delete_role error]: {e}")
            return False

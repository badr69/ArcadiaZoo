from app.db.psql import get_db_connection


class Role:
    def __init__(self, id, name, created_at=None, update_at=None):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.update_at = update_at

    def __repr__(self):
        return f"<Role id={self.id} name={self.name}>"

class RoleModel:

    @classmethod
    def list_all_roles(cls):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name, created_at, updated_at FROM roles")
            rows = cur.fetchall()
            roles = [Role(id=row[0], name=row[1], created_at=row[2]) for row in rows]
            return roles
        except Exception as e:
            print(f"Erreur lors de la récupération des rôles : {e}")
            return []
        finally:
            if cur: cur.close()
            if conn: conn.close()

    @staticmethod
    def get_role_by_id(role_id: int):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name, created_at, updated_at FROM roles WHERE id = %s", (role_id,))
            row = cur.fetchone()
            if row:
                return Role(id=row[0], name=row[1], created_at=row[2])
            return None
        except Exception as e:
            print(f"[get_role_by_id error]: {e}")
            return None
        finally:
            if cur: cur.close()
            if conn: conn.close()

    @staticmethod
    def create_role(name: str):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO roles (name) VALUES (%s)", (name,))
            conn.commit()
            return True
        except Exception as e:
            print(f"[create_role error]: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if cur: cur.close()
            if conn: conn.close()


    @staticmethod
    def update_role(role_id: int, name: str):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("UPDATE roles SET name = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (name, role_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"[update_role error]: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if cur: cur.close()
            if conn: conn.close()

    @staticmethod
    def delete_role(role_id: int):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM roles WHERE id = %s", (role_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"[delete_role error]: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if cur: cur.close()
            if conn: conn.close()

from werkzeug.security import generate_password_hash
from app.db.psql import get_db_connection

class UserModel:
    def __init__(self, id, username, email, password_hash=None, role_id=None, role_name=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role_id = role_id
        self.role_name = role_name
        self.created_at = created_at

    @classmethod
    def get_by_email(cls, email):
        conn = cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT u.id, u.username, u.email, u.password, u.role_id, r.name AS role_name, u.created_at
                FROM users u
                LEFT JOIN roles r ON u.role_id = r.id
                WHERE u.email = %s
            """, (email,))
            row = cur.fetchone()
            if row:
                return cls(*row)
            return None
        except Exception as e:
            print(f"[get_by_email error]: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def get_user_by_id(cls, user_id):
        conn = cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT u.id, u.username, u.email, u.password, u.role_id, r.name AS role_name, u.created_at
                FROM users u
                LEFT JOIN roles r ON u.role_id = r.id
                WHERE u.id = %s
            """, (user_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
            return None
        except Exception as e:
            print(f"[get_user_by_id error]: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def list_all_users(cls):
        conn = cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT u.id, u.username, u.email, u.password, u.role_id, r.name AS role_name, u.created_at
                FROM users u
                LEFT JOIN roles r ON u.role_id = r.id
            """)
            rows = cur.fetchall()
            return [cls(*row) for row in rows]
        except Exception as e:
            print(f"[list_all_users error]: {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def create_user(username, email, password, role_id):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            hashed_password = generate_password_hash(password)  # si tu utilises Werkzeug
            cur.execute("""
                        INSERT INTO users (username, email, password, role_id)
                        VALUES (%s, %s, %s, %s)
                        """, (username, email, hashed_password, role_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la création de l'utilisateur : {e}")
            return False
        finally:
            cur.close()
            conn.close()

    #
    @classmethod
    def delete_user(cls, user_id):
        conn = cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"[delete_user error]: {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

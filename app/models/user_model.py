from app.db.psql import get_db_connection
from flask_login import UserMixin
from app.utils.security import verify_password, hash_password


class UserModel(UserMixin):
    def __init__(self, user_id=None, username=None, email=None, password_hash=None,
                 role_id=None, role_name=None, created_at=None, updated_at=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role_id = role_id
        self.role_name = role_name
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def id(self):
        return self.user_id

    @property
    def role(self):
        return self.role_id


    # ===================== AUTHENTICATION =====================
    @classmethod
    def authenticate(cls, email, password):
        user = cls.get_user_by_email(email)
        if user and verify_password(user.password_hash, password):
            return user
        return None

    # ===================== READ =====================
    @classmethod
    def get_user_by_email(cls, email):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT u.user_id, u.username, u.email, u.password_hash, u.role_id, r.name AS role_name,
                               u.created_at, u.updated_at
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.role_id
                        WHERE u.email = %s
                    """, (email,))
                    row = cur.fetchone()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"[get_by_email error]: {e}")
            return None

    @classmethod
    def get_user_by_id(cls, user_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT u.user_id, u.username, u.email, u.password_hash, u.role_id, r.name AS role_name,
                               u.created_at, u.updated_at
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.role_id
                        WHERE u.user_id = %s
                    """, (user_id,))
                    row = cur.fetchone()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"[get_user_by_id error]: {e}")
            return None

    @classmethod
    def list_all_users(cls):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT u.user_id, u.username, u.email, u.password_hash, u.role_id, r.name AS role_name,
                               u.created_at, u.updated_at
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.role_id
                        ORDER BY u.user_id
                    """)
                    rows = cur.fetchall()
                    return [cls(*row) for row in rows]
        except Exception as e:
            print(f"[list_all_users error]: {e}")
            return []

    # ===================== CREATE =====================
    @classmethod
    def create_user(cls, username, email, password, role_id):
        password_hash = hash_password(password)
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO users (username, email, password_hash, role_id)
                        VALUES (%s, %s, %s, %s)
                        RETURNING user_id
                    """, (username, email, password_hash, role_id))
                    user_id = cur.fetchone()[0]
                    conn.commit()
                    return cls.get_user_by_id(user_id)
        except Exception as e:
            print(f"[create error]: {e}")
            return None

    # ===================== UPDATE =====================
    def update_user(self, username=None, email=None, role_id=None):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE users
                        SET username = %s,
                            email = %s,
                            role_id = %s,
                            updated_at = NOW()
                        WHERE user_id = %s
                    """, (
                        username if username else self.username,
                        email if email else self.email,
                        role_id if role_id else self.role_id,
                        self.user_id
                    ))

                    if cur.rowcount == 0:
                        return {"error": "Utilisateur non trouvé."}, 404

                    conn.commit()

                    # Mise à jour des attributs de l'objet
                    if username: self.username = username
                    if email: self.email = email
                    if role_id:
                        self.role_id = role_id
                        # On récupère le role_name pour l'objet
                        cur.execute("SELECT name FROM roles WHERE role_id = %s", (role_id,))
                        self.role_name = cur.fetchone()[0] if cur.rowcount > 0 else None

                    return {"message": "Utilisateur mis à jour."}, 200
        except Exception as e:
            print(f"[update error]: {e}")
            return {"error": "Erreur serveur."}, 500

    # ===================== DELETE =====================
    def delete_user(self):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM users WHERE user_id = %s", (self.user_id,))
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"[delete error]: {e}")
            return False

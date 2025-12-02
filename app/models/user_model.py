from app.db.psql import get_db_connection
from flask_login import UserMixin
from datetime import datetime


class UserModel(UserMixin):
    def __init__(self, user_id, username, email, password_hash,
                 role_id, role_name, created_at=None, updated_at=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role_id = role_id
        self.role_name = role_name
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    @property
    def id(self):
        return self.user_id

    # ========================
    # ======= READ ===========
    # ========================
    @classmethod
    def list_all_users(cls):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT u.user_id, u.username, u.email, u.password_hash,
                               u.role_id, r.name AS role_name,
                               u.created_at, u.updated_at
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.role_id
                        ORDER BY u.user_id
                    """)
                    rows = cur.fetchall()
                    return [cls(*row) for row in rows]
        except Exception as e:
            print(f"[UserModel.list_all_users] Error: {e}")
            return []

    @classmethod
    def list_all_vets(cls):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT u.user_id, u.username, u.email, u.password_hash,
                               u.role_id, r.name AS role_name,
                               u.created_at, u.updated_at
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.role_id
                        WHERE r.name = 'vet'
                        ORDER BY u.username
                    """)
                    rows = cur.fetchall()
                    return [cls(*row) for row in rows]
        except Exception as e:
            print(f"[UserModel.list_all_vets] Error: {e}")
            return []

    @classmethod
    def list_all_employees(cls):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT u.user_id, u.username, u.email, u.password_hash,
                               u.role_id, r.name AS role_name,
                               u.created_at, u.updated_at
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.role_id
                        WHERE r.name = 'employee'
                        ORDER BY u.username
                    """)
                    rows = cur.fetchall()
                    return [cls(*row) for row in rows]
        except Exception as e:
            print(f"[UserModel.list_all_employees] Error: {e}")
            return []

    @classmethod
    def get_user_by_id(cls, user_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT u.user_id, u.username, u.email, u.password_hash,
                               u.role_id, r.name AS role_name,
                               u.created_at, u.updated_at
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.role_id
                        WHERE u.user_id = %s
                    """, (user_id,))
                    row = cur.fetchone()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"[UserModel.get_user_by_id] Error: {e}")
            return None

    @classmethod
    def get_user_by_email(cls, email):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT u.user_id, u.username, u.email, u.password_hash,
                               u.role_id, r.name AS role_name,
                               u.created_at, u.updated_at
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.role_id
                        WHERE u.email = %s
                    """, (email,))
                    row = cur.fetchone()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"[UserModel.get_user_by_email] Error: {e}")
            return None

    # ========================
    # ======= CREATE =========
    # ========================
    @classmethod
    def create_user(cls, username, email, password_hash, role_id):
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
            print(f"[UserModel.create_user] Error: {e}")
            return None

    # ========================
    # ======= UPDATE =========
    # ========================
    def update_user(self, username, email, role_id, password_hash=None):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    if password_hash:
                        cur.execute("""
                            UPDATE users
                            SET username = %s,
                                email = %s,
                                role_id = %s,
                                password_hash = %s,
                                updated_at = NOW()
                            WHERE user_id = %s
                        """, (username, email, role_id, password_hash, self.user_id))
                    else:
                        cur.execute("""
                            UPDATE users
                            SET username = %s,
                                email = %s,
                                role_id = %s,
                                updated_at = NOW()
                            WHERE user_id = %s
                        """, (username, email, role_id, self.user_id))
                    if cur.rowcount == 0:
                        return False
                    conn.commit()
                    return True
        except Exception as e:
            print(f"[UserModel.update_user] Error: {e}")
            return False

    # ========================
    # ======= DELETE =========
    # ========================
    def delete_user(self):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM users WHERE user_id = %s", (self.user_id,))
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"[UserModel.delete_user] Error: {e}")
            return False







# from app.db.psql import get_db_connection
# from flask_login import UserMixin
#
#
# class UserModel(UserMixin):
#     def __init__(self, user_id, username, email, password_hash,
#                  role_id, role_name, created_at=None, updated_at=None
#     ):
#         self.user_id = user_id
#         self.username = username
#         self.email = email
#         self.password_hash = password_hash
#         self.role_id = role_id
#         self.role_name = role_name
#         self.created_at = created_at
#         self.updated_at = updated_at
#
#     @property
#     def id(self):
#         return self.user_id
#
#     # ====================================
#     # ==========     READ     ============
#     # ====================================
#     @classmethod
#     def list_all_users(cls):
#         try:
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute("""
#                         SELECT u.user_id, u.username, u.email, u.password_hash,
#                                u.role_id, r.name AS role_name,
#                                u.created_at, u.updated_at
#                         FROM users u
#                         LEFT JOIN roles r ON u.role_id = r.role_id
#                         ORDER BY u.user_id
#                     """)
#
#                     rows = cur.fetchall()
#                     return [cls(*row) for row in rows]
#
#         except Exception as e:
#             print(f"[UserModel.list_all_users] Error: {e}")
#             return []
#
#     @classmethod
#     def list_all_vets(cls):
#         """
#         Retourne tous les utilisateurs dont le rôle est 'vet'.
#         Retour : liste d'objets UserModel
#         """
#         try:
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute("""
#                         SELECT u.user_id, u.username, u.email, u.password_hash,
#                                u.role_id, r.name AS role_name,
#                                u.created_at, u.updated_at
#                         FROM users u
#                         LEFT JOIN roles r ON u.role_id = r.role_id
#                         WHERE r.name = 'vet'
#                         ORDER BY u.username
#                     """)
#                     rows = cur.fetchall()
#                     return [cls(*row) for row in rows]
#
#         except Exception as e:
#             print(f"[UserModel.list_all_vets] Error: {e}")
#             return []
#
#     @classmethod
#     def list_all_employees(cls):
#         """
#         Retourne tous les utilisateurs dont le rôle est 'employee'.
#         Retour : liste d'objets UserModel
#         """
#         try:
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute("""
#                         SELECT u.user_id, u.username, u.email, u.password_hash,
#                                u.role_id, r.name AS role_name,
#                                u.created_at, u.updated_at
#                         FROM users u
#                         LEFT JOIN roles r ON u.role_id = r.role_id
#                         WHERE r.name = 'employee'
#                         ORDER BY u.username
#                     """)
#                     rows = cur.fetchall()
#                     return [cls(*row) for row in rows]
#         except Exception as e:
#             print(f"[UserModel.list_all_employees] Error: {e}")
#             return []
#
#
#     @classmethod
#     def get_user_by_id(cls, user_id):
#         try:
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute("""
#                         SELECT u.user_id, u.username, u.email, u.password_hash,
#                                u.role_id, r.name AS role_name,
#                                u.created_at, u.updated_at
#                         FROM users u
#                         LEFT JOIN roles r ON u.role_id = r.role_id
#                         WHERE u.user_id = %s
#                     """, (user_id,))
#                     row = cur.fetchone()
#                     return cls(*row) if row else None
#
#         except Exception as e:
#             print(f"[UserModel.get_user_by_id] Error: {e}")
#             return None
#
#     @classmethod
#     def get_user_by_email(cls, email):
#         try:
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute("""
#                         SELECT u.user_id, u.username, u.email, u.password_hash,
#                                u.role_id, r.name AS role_name,
#                                u.created_at, u.updated_at
#                         FROM users u
#                         LEFT JOIN roles r ON u.role_id = r.role_id
#                         WHERE u.email = %s
#                     """, (email,))
#
#                     row = cur.fetchone()
#                     return cls(*row) if row else None
#
#         except Exception as e:
#             print(f"[UserModel.get_user_by_email] Error: {e}")
#             return None
#
#
#
#     # ====================================
#     # ==========    CREATE    ============
#     # ====================================
#     @classmethod
#     def create_user(cls, username, email, password_hash, role_id):
#         """ATTENTION : ici nous ne hashons pas.
#         Le mot de passe est déjà hashé dans UserService."""
#         try:
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute("""
#                         INSERT INTO users (username, email, password_hash, role_id)
#                         VALUES (%s, %s, %s, %s)
#                         RETURNING user_id
#                     """, (username, email, password_hash, role_id))
#
#                     user_id = cur.fetchone()[0]
#                     conn.commit()
#                     return cls.get_user_by_id(user_id)
#         except Exception as e:
#             print(f"[UserModel.create_user] Error: {e}")
#             return None
#
#     # ====================================
#     # ==========    UPDATE    ============
#     # ====================================
#     def update_user(self, username, email, role_id, password_hash=None):
#         """Modifie uniquement les données — aucune logique métier ici."""
#         try:
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     if password_hash:
#                         # Met à jour aussi le mot de passe
#                         cur.execute("""
#                                     UPDATE users
#                                     SET username      = %s,
#                                         email         = %s,
#                                         role_id       = %s,
#                                         password_hash = %s,
#                                         updated_at    = NOW()
#                                     WHERE user_id = %s
#                                     """, (username, email, role_id, password_hash, self.user_id))
#                     else:
#                         # Pas de modification du mot de passe
#                         cur.execute("""
#                                     UPDATE users
#                                     SET username   = %s,
#                                         email      = %s,
#                                         role_id    = %s,
#                                         updated_at = NOW()
#                                     WHERE user_id = %s
#                                     """, (username, email, role_id, self.user_id))
#
#                     if cur.rowcount == 0:
#                         return False
#                     conn.commit()
#                     return True
#         except Exception as e:
#             print(f"[UserModel.update_user] Error: {e}")
#             return False
#
#     # ====================================
#     # ==========    DELETE    ============
#     # ====================================
#     def delete_user(self):
#         try:
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute("""
#                         DELETE FROM users
#                         WHERE user_id = %s
#                     """, (self.user_id,))
#
#                     conn.commit()
#                     return cur.rowcount > 0
#
#         except Exception as e:
#             print(f"[UserModel.delete_user] Error: {e}")
#             return False
#
#
#
#
#
#

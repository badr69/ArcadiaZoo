from werkzeug.security import generate_password_hash
from app.db.psql import get_db_connection
import psycopg2  # Assure-toi que psycopg2 est bien importé

class UserModel:
    def __init__(self, id, username, email, password_hash=None, role_id=None, role_name=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role_id = role_id
        self.role_name = role_name
        self.created_at = created_at

    # ========== GETTERS (instanciation d'un objet) ==========

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
            return cls(*row) if row else None
        except Exception as e:
            print(f"[get_by_email error]: {e}")
            return None
        finally:
            if cur: cur.close()
            if conn: conn.close()

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
            return cls(*row) if row else None
        except Exception as e:
            print(f"[get_user_by_id error]: {e}")
            return None
        finally:
            if cur: cur.close()
            if conn: conn.close()

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
            if cur: cur.close()
            if conn: conn.close()

    # ========== CREATE / UPDATE / DELETE ==========

    @staticmethod
    def create_user(username, email, password, role_id):
        conn = cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            hashed_password = generate_password_hash(password)
            cur.execute("""
                INSERT INTO users (username, email, password, role_id)
                VALUES (%s, %s, %s, %s)
            """, (username, email, hashed_password, role_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"[create_user error]: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if cur: cur.close()
            if conn: conn.close()

    @staticmethod
    def update_user(user_id: int, username: str, email: str, role_id: int):
        conn = cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Vérifie que le rôle existe
            cur.execute("SELECT id FROM roles WHERE id = %s", (role_id,))
            if cur.fetchone() is None:
                return {"error": "Rôle inexistant."}, 400

            cur.execute("""
                UPDATE users
                SET username = %s,
                    email    = %s,
                    role_id  = %s
                WHERE id = %s
            """, (username, email, role_id, user_id))

            if cur.rowcount == 0:
                return {"error": "Utilisateur non trouvé."}, 404

            conn.commit()
            return {"message": "Utilisateur mis à jour."}, 200
        except psycopg2.Error as db_err:
            print("[PostgreSQL] update_user:", db_err)
            if conn: conn.rollback()
            return {"error": "Erreur PostgreSQL."}, 500
        except Exception as exc:
            print("[Exception] update_user:", exc)
            if conn: conn.rollback()
            return {"error": "Erreur serveur."}, 500
        finally:
            if cur: cur.close()
            if conn: conn.close()

    @staticmethod
    def delete_user(user_id):
        conn = cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"[delete_user error]: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if cur: cur.close()
            if conn: conn.close()



# from werkzeug.security import generate_password_hash
# from app.db.psql import get_db_connection
#
# class UserModel:
#     def __init__(self, id, username, email, password_hash=None, role_id=None, role_name=None, created_at=None):
#         self.id = id
#         self.username = username
#         self.email = email
#         self.password_hash = password_hash
#         self.role_id = role_id
#         self.role_name = role_name
#         self.created_at = created_at
#
#     @classmethod
#     def get_by_email(cls, email):
#         conn = cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("""
#                 SELECT u.id, u.username, u.email, u.password, u.role_id, r.name AS role_name, u.created_at
#                 FROM users u
#                 LEFT JOIN roles r ON u.role_id = r.id
#                 WHERE u.email = %s
#             """, (email,))
#             row = cur.fetchone()
#             if row:
#                 return cls(*row)
#             return None
#         except Exception as e:
#             print(f"[get_by_email error]: {e}")
#             return None
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#
#     @classmethod
#     def get_user_by_id(cls, user_id):
#         conn = cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("""
#                 SELECT u.id, u.username, u.email, u.password, u.role_id, r.name AS role_name, u.created_at
#                 FROM users u
#                 LEFT JOIN roles r ON u.role_id = r.id
#                 WHERE u.id = %s
#             """, (user_id,))
#             row = cur.fetchone()
#             if row:
#                 return cls(*row)
#             return None
#         except Exception as e:
#             print(f"[get_user_by_id error]: {e}")
#             return None
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#
#     @classmethod
#     def list_all_users(cls):
#         conn = cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("""
#                 SELECT u.id, u.username, u.email, u.password, u.role_id, r.name AS role_name, u.created_at
#                 FROM users u
#                 LEFT JOIN roles r ON u.role_id = r.id
#             """)
#             rows = cur.fetchall()
#             return [cls(*row) for row in rows]
#         except Exception as e:
#             print(f"[list_all_users error]: {e}")
#             return []
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#
#     @staticmethod
#     def create_user(username, email, password, role_id):
#         conn = get_db_connection()
#         cur = conn.cursor()
#         try:
#             hashed_password = generate_password_hash(password)  # si tu utilises Werkzeug
#             cur.execute("""
#                         INSERT INTO users (username, email, password, role_id)
#                         VALUES (%s, %s, %s, %s)
#                         """, (username, email, hashed_password, role_id))
#             conn.commit()
#             return True
#         except Exception as e:
#             print(f"Erreur lors de la création de l'utilisateur : {e}")
#             return False
#         finally:
#             cur.close()
#             conn.close()
#
#
#     @staticmethod
#     def update_user(user_id: int, username: str, email: str, role_id: int):
#
#         conn = cur = None
#         try:
#             # ---------- validation de l'existence du rôle ----------
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("SELECT id FROM roles WHERE id = %s", (role_id,))
#             if cur.fetchone() is None:
#                 return {"error": "Rôle inexistant."}, 400
#
#             # ---------- mise à jour ----------
#             with conn.cursor() as cur2:
#                 cur2.execute("""
#                     UPDATE users
#                     SET username = %s,
#                         email    = %s,
#                         role_id  = %s
#                     WHERE id = %s
#                     RETURNING id
#                 """, (username, email, role_id, user_id))
#                 if cur2.rowcount == 0:
#                     return {"error": "User Not found."}, 404
#
#             conn.commit()
#             return {"message": "User updated."}, 200
#
#         except psycopg2.Error as db_err:
#             print("[PostgreSQL] update_user:", db_err)
#             if conn:
#                 conn.rollback()
#             return {"error": "Erreur when update."}, 500
#         except Exception as exc:
#             print("[Service] update_user:", exc)
#             if conn:
#                 conn.rollback()
#             return {"error": "Server Error."}, 500
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#
#
#     @classmethod
#     def delete_user(cls, user_id):
#         conn = cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
#             conn.commit()
#             return cur.rowcount > 0
#         except Exception as e:
#             print(f"[delete_user error]: {e}")
#             return False
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()

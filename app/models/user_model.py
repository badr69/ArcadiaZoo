from werkzeug.security import generate_password_hash
from app.db.psql import get_db_connection



class User:
    def __init__(self, id, username, email, password_hash=None, role_name=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role_name = role_name
        self.created_at = created_at


    @classmethod
    def get_by_email(cls, email):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, username, email, password, role_id FROM users WHERE email = %s", (email,))
            row = cur.fetchone()
            if row:
                return cls(*row)  # Crée un objet User avec les données
            return None
        except Exception as e:
            print(f"Erreur get_by_email: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


    @classmethod
    def create(cls, username, email, password, role_id):
        password = generate_password_hash(password)
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO users (username, email, password, role_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (username, email, password, role_id))
            user_id = cur.fetchone()[0]
            conn.commit()
            return cls(user_id, username, email, password, role_id)
        finally:
            cur.close()
            conn.close()
# TODO get all users
    @classmethod
    def get_all_users(cls):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                        SELECT u.id, u.username, u.email, r.name, u.created_at
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.id
                        """)
            rows = cur.fetchall()
            users = []
            for row in rows:
                user_id, username, email, role_name, created_at = row
                users.append(cls(user_id, username, email, None, role_name, created_at))
            return users
        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            return None
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
    # TODO Find user by its id
    @classmethod
    def get_user_by_id(cls, id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                        SELECT u.id, u.username, u.email, r.name AS role_name, u.created_at
                        FROM users u
                        LEFT JOIN roles r ON u.role_id = r.id
                        WHERE u.id = %s
                        """, (id,))
            row = cur.fetchone()  # une seule ligne (tuple) ou None
            if row is None:
                return None  # pas trouvé
            user_id, username, email, role_name, created_at = row
            return cls(user_id, username, email, None, role_name=role_name, created_at=created_at)
        except Exception as e:
            print(f"Erreur lors de la récupération de l'utilisateur : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

# TODO update_user
#class UserService:
    @staticmethod
    def update_user(id, username, email, role_name):
            try:
                success = User.update_user(id, username, email, role_name)
                if not success:
                    # Ici on peut différencier selon le message du modèle ou customiser
                    return {
                        "status": False,
                        "message": f"La mise à jour a échoué, soit l'utilisateur ou le rôle n'a pas été trouvé."
                    }
                return {
                    "status": True,
                    "message": "Utilisateur mis à jour avec succès."
                }
            except Exception as e:
                # Log l'erreur ou autre traitement
                return {
                    "status": False,
                    "message": f"Erreur lors de la mise à jour de l'utilisateur : {str(e)}"
                }

    # TODO delete user
    @classmethod
    def delete_user(cls, id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id = %s", (id,))
            conn.commit()
            if cur.rowcount == 0:
                print(f"Aucun utilisateur trouvé avec l'id {id}.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'utilisateur : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

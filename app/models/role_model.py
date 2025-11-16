from app.db.psql import get_db_connection


class RoleModel:
    def __init__(self, role_id, name):
        self.role_id = role_id
        self.name = name

    def __repr__(self):
        return f"<Role id={self.role_id} name={self.name}>"

    @property
    def id(self):
        return self.role_id

    @classmethod
    def list_all_roles(cls):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM roles")
            rows = cur.fetchall()

            roles = [Role(id=row[0], name=row[1]) for row in rows]  # créer les objets Role
            return roles
        except Exception as e:
            print(f"Erreur lors de la récupération des rôles : {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()





# from app.db.psql import get_db_connection
#
#
#
# class RoleModel():
#
#     @classmethod
#     def get_all_roles(cls):
#         conn = None
#         cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("SELECT id, name FROM roles")
#             roles = cur.fetchall()
#             return roles  # liste de tuples (id, name)
#         except Exception as e:
#             print(f"Erreur lors de la récupération des rôles : {e}")
#             return []
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()

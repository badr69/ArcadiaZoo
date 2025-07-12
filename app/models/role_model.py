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

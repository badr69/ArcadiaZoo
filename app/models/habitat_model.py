from app.db.psql import get_db_connection


class Habitat:
    def __init__(self, habitat_id, name, url_image, description, created_at=None, updated_at=None):
        self.habitat_id = habitat_id
        self.name = name
        self.url_image = url_image
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def id(self):
        return self.habitat_id

    @classmethod
    def list_all_habitats(cls):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT id, name, url_image, description, created_at, updated_at FROM habitats ORDER BY id"
                    )
                    rows = cur.fetchall()
                    return [cls(*row) for row in rows]
        except Exception as e:
            print(f"Erreur lors de la récupération des habitats : {e}")
            return []

    @classmethod
    def get_habitat_by_id(cls, habitat_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, name, url_image, description, created_at, updated_at
                        FROM habitats
                        WHERE id = %s
                    """, (habitat_id,))
                    row = cur.fetchone()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"Erreur lors de la récupération de l'habitat par id : {e}")
            return None

    @classmethod
    def create_habitat(cls, name, url_image, description):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO habitats (name, url_image, description)
                        VALUES (%s, %s, %s)
                        RETURNING id, created_at
                    """, (name, url_image, description))
                    habitat_id, created_at = cur.fetchone()
                    conn.commit()
                    return cls(habitat_id, name, url_image, description, created_at)
        except Exception as e:
            print(f"Erreur lors de la création d'un habitat : {e}")
            return None

    @classmethod
    def update_habitat(cls, habitat_id, name, url_image, description):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE habitats
                        SET name = %s,
                            url_image = %s,
                            description = %s,
                            updated_at=NOW()
                        WHERE id = %s
                    """, (name, url_image, description, habitat_id))
                    conn.commit()
                    return cls(habitat_id, name, url_image, description) if cur.rowcount > 0 else None
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'habitat : {e}")
            return None

    @classmethod
    def delete_habitat(cls, habitat_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM habitats WHERE id = %s", (habitat_id,))
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la suppression de l'habitat : {e}")
            return False








#
# from app.db.psql import get_db_connection
#
#
# class Habitat:
#     def __init__(self, id, name, url_image, description, created_at=None, updated_at=None):
#         self.habitat = id
#         self.name = name
#         self.url_image = url_image
#         self.description = description
#         self.created_at = created_at
#         self.updated_at = updated_at
#
#   #
#     @classmethod
#     def list_all_habitats(cls):
#         conn = None
#         cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("SELECT id, name, url_image, description, created_at, updated_at FROM habitats ORDER BY id")
#             rows = cur.fetchall()
#             print(rows)  # Pour voir l’ordre des colonnes et des valeurs
#             habitats = []
#             for row in rows:
#                 habitat = cls(*row)
#                 habitats.append(habitat)
#             return habitats
#         except Exception as e:
#             print(f"Erreur lors de la récupération des habitats : {e}")
#             return []
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#
#     @classmethod
#     def get_habitat_by_id(cls, habitat_id):
#         conn = None
#         cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("""
#                         SELECT id, name, url_image, description, created_at, updated_at
#                         FROM habitats
#                         WHERE id = %s
#                         """, (habitat_id,))
#             row = cur.fetchone()
#             if row:
#                 return cls(*row)
#             return None
#         except Exception as e:
#             print(f"Erreur lors de la récupération de l'habitat par id : {e}")
#             return None
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#
#     @staticmethod
#     def create_habitat(name, url_image, description):
#         conn = None
#         cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("""
#                         INSERT INTO habitats (name, url_image, description)
#                         VALUES (%s, %s, %s) RETURNING id, created_at
#                         """, (name, url_image, description))
#             row = cur.fetchone()
#             conn.commit()
#             habitat_id, created_at = row
#             return Habitat(habitat_id, name, url_image, description, created_at)
#         except Exception as e:
#             print(f"Erreur lors de la création d'un habitat : {e}")
#             return None
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#
#     @staticmethod
#     def update_habitat(habitat_id, name, url_image, description):
#         conn = None
#         cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("""
#                         UPDATE habitats
#                         SET name=%s,
#                             url_image=%s,
#                             description=%s,
#                             updated_at=NOW()
#                         WHERE id = %s
#                         """, (name, url_image, description, habitat_id))
#             conn.commit()
#             return cur.rowcount > 0
#         except Exception as e:
#             print(f"Erreur lors de la mise à jour de l'habitat : {e}")
#             return False
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#
#     @staticmethod
#     def delete_habitat(habitat_id):
#         conn = None
#         cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("DELETE FROM habitats WHERE id = %s", (habitat_id,))
#             conn.commit()
#             return cur.rowcount > 0
#         except Exception as e:
#             print(f"Erreur lors de la suppression de l'habitat : {e}")
#             return False
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()

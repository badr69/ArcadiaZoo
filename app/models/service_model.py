from app.db.psql import get_db_connection

class ServiceModel:
    def __init__(self, service_id, name, url_image, description, created_at=None, updated_at=None):
        self.service_id = service_id
        self.name = name
        self.url_image = url_image
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def id(self):
        return self.service_id


    # ================== CREATE ==================

    @classmethod
    def create_service(cls, name, url_image, description):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO services (name, url_image, description)
                        VALUES (%s, %s, %s)
                        RETURNING id, created_at
                    """, (name, url_image, description))
                    row = cur.fetchone()
                    conn.commit()
                    if row:
                        service_id, created_at = row
                        return cls(service_id, name, url_image, description, created_at)
                    return None
        except Exception as e:
            print(f"[create_service error]: {e}")
            return None

    # ================== READ ==================

    @classmethod
    def list_all_services(cls):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, name, url_image, description, created_at, updated_at
                        FROM services
                        ORDER BY id
                    """)
                    rows = cur.fetchall()
                    return [cls(*row) for row in rows]
        except Exception as e:
            print(f"[list_all_services error]: {e}")
            return []

    @classmethod
    def get_service_by_id(cls, service_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, name, url_image, description, created_at, updated_at
                        FROM services
                        WHERE id = %s
                    """, (service_id,))
                    row = cur.fetchone()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"[get_service_by_id error]: {e}")
            return None

    # ================== UPDATE ==================

    @classmethod
    def update_service(cls, service_id, name, url_image, description):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE services
                        SET name = %s,
                            url_image = %s,
                            description = %s,
                            updated_at = NOW()
                        WHERE id = %s
                    """, (name, url_image, description, service_id))
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"[update_service error]: {e}")
            return False

    # ================== DELETE ==================

    @classmethod
    def delete_service(cls, service_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM services WHERE id = %s", (service_id,))
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"[delete_service error]: {e}")
            return False







# from app.db.psql import get_db_connection
#
#
# class ServiceModel:
#     def __init__(self, id, name, url_image, description, created_at=None, updated_at=None):
#         self.id = id
#         self.name = name
#         self.url_image = url_image
#         self.description = description
#         self.created_at = created_at
#         self.updated_at = updated_at
#
#     @classmethod
#     def create_service(cls, name, url_image, description):
#         conn = None
#         cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("""
#                 INSERT INTO services (name, url_image, description)
#                 VALUES (%s, %s, %s)
#                 RETURNING id, created_at
#             """, (name, url_image, description))
#             row = cur.fetchone()
#             print("Resultat RETURNING :", row)
#             conn.commit()
#             service_id, created_at = row
#             return cls(service_id, name, url_image, description)
#
#         except Exception as e:
#             print(f"Erreur lors de la création d'un services : {e}")
#             return None
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#
#     @classmethod
#     def list_all_services(cls):
#         conn = None
#         cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("SELECT id, name, url_image, description, created_at, updated_at FROM services ORDER BY id")
#             rows = cur.fetchall()
#             services = []
#             for row in rows:
#                 service = cls(*row)
#                 services.append(service)
#             return services
#         except Exception as e:
#             print(f"Erreur lors de la récupération des servicess : {e}")
#             return []
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#
#     @classmethod
#     def get_service_by_id(cls, service_id):
#         conn = None
#         cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("""
#                 SELECT id, name, url_image, description, created_at, updated_at
#                 FROM services WHERE id = %s
#             """, (service_id,))
#             row = cur.fetchone()
#             if row:
#                 return cls(*row)
#             return None
#         except Exception as e:
#             print(f"Erreur lors de la récupération de l'services par id : {e}")
#             return None
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#
#     @classmethod
#     def update_service(cls, services_id, name, url_image, description):
#         conn = None
#         cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("""
#                 UPDATE services
#                 SET name=%s, url_image=%s, description=%s, updated_at=NOW()
#                 WHERE id=%s
#             """, (name, description, url_image, services_id))
#             conn.commit()
#             if cur.rowcount == 0:
#                 print(f"Aucun services trouvé avec l'id {services_id} pour mise à jour.")
#                 return False
#             return True
#         except Exception as e:
#             print(f"Erreur lors de la mise à jour de l'services : {e}")
#             return False
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()
#
#     @classmethod
#     def delete_service(cls, services_id):
#         conn = None
#         cur = None
#         try:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("DELETE FROM services WHERE id = %s", (services_id,))
#             conn.commit()
#             if cur.rowcount == 0:
#                 print(f"Aucun services trouvé avec l'id {services_id} à supprimer.")
#                 return False
#             return True
#         except Exception as e:
#             print(f"Erreur lors de la suppression de l'services : {e}")
#             return False
#         finally:
#             if cur:
#                 cur.close()
#             if conn:
#                 conn.close()

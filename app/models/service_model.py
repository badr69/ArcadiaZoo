{"variant":"standard","id":"67126"}
from app.db.psql import get_db_connection

class ServiceModel:
    """Modèle pour gérer les services."""

    def __init__(self, service_id, name, description, url_image=None, created_at=None, updated_at=None):
        self.service_id = service_id
        self.name = name
        self.description = description
        self.url_image = url_image
        self.created_at = created_at
        self.updated_at = updated_at

    # ===================== READ =====================
    @classmethod
    def list_all_services(cls):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT service_id, name, description, url_image, created_at, updated_at
                        FROM services
                        ORDER BY service_id
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
                        SELECT service_id, name, description, url_image, created_at, updated_at
                        FROM services
                        WHERE service_id = %s
                    """, (service_id,))
                    row = cur.fetchone()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"[get_service_by_id error]: {e}")
            return None

    # ===================== CREATE =====================
    @classmethod
    def create_service(cls, name, description, url_image=None):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT service_id FROM services WHERE name = %s", (name,))
                    if cur.fetchone():
                        print(f"[create_service warning]: Nom déjà existant: {name}")
                        return None

                    cur.execute("""
                        INSERT INTO services (name, description, url_image)
                        VALUES (%s, %s, %s)
                        RETURNING service_id, created_at
                    """, (name, description, url_image))
                    service_id, created_at = cur.fetchone()
                    conn.commit()
                    return cls(service_id, name, description, url_image, created_at)
        except Exception as e:
            print(f"[create_service error]: {e}")
            return None

    # ===================== UPDATE =====================
    def update_service(self, name, description, url_image=None):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT service_id FROM services 
                        WHERE name = %s AND service_id != %s
                    """, (name, self.service_id))
                    if cur.fetchone():
                        print(f"[update_service warning]: Nom déjà utilisé: {name}")
                        return False

                    cur.execute("""
                        UPDATE services
                        SET name = %s, description = %s, url_image = %s, updated_at=NOW()
                        WHERE service_id=%s
                    """, (name, description, url_image, self.service_id))
                    conn.commit()

                    self.name = name
                    self.description = description
                    self.url_image = url_image
                    return True
        except Exception as e:
            print(f"[update_service error]: {e}")
            return False

    # ===================== DELETE =====================
    def delete_service(self):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM services WHERE service_id = %s", (self.service_id,))
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"[delete_service error]: {e}")
            return False

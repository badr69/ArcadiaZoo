from app.db.psql import get_db_connection


class ServiceModel:
    def __init__(self, id, name, url_image, description, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.url_image = url_image
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_service(cls, name, url_image, description):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO services (name, url_image, description)
                VALUES (%s, %s, %s)
                RETURNING id, created_at
            """, (name, url_image, description))
            row = cur.fetchone()
            print("Resultat RETURNING :", row)
            conn.commit()
            service_id, created_at = row
            return cls(service_id, name, url_image, description)

        except Exception as e:
            print(f"Erreur lors de la création d'un services : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def list_all_services(cls):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name, url_image, description, created_at, updated_at FROM services ORDER BY id")
            rows = cur.fetchall()
            services = []
            for row in rows:
                service = cls(*row)
                services.append(service)
            return services
        except Exception as e:
            print(f"Erreur lors de la récupération des servicess : {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def get_service_by_id(cls, service_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, name, url_image, description, created_at, updated_at
                FROM services WHERE id = %s
            """, (service_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération de l'services par id : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def update_service(cls, services_id, name, url_image, description):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE services
                SET name=%s, url_image=%s, description=%s, updated_at=NOW()
                WHERE id=%s
            """, (name, description, url_image, services_id))
            conn.commit()
            if cur.rowcount == 0:
                print(f"Aucun services trouvé avec l'id {services_id} pour mise à jour.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'services : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def delete_service(cls, services_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM services WHERE id = %s", (services_id,))
            conn.commit()
            if cur.rowcount == 0:
                print(f"Aucun services trouvé avec l'id {services_id} à supprimer.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'services : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

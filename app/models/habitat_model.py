from app.db.psql import get_db_connection


class Habitat:
    def __init__(self, id, name, url_image, description, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.url_image = url_image
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_habitat(cls, name, url_image, description):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO habitats (name, url_image, description)
                VALUES (%s, %s, %s)
                RETURNING id, created_at
            """, (name, url_image, description))
            row = cur.fetchone()
            print("Resultat RETURNING :", row)
            conn.commit()
            habitat_id, created_at = row
            return cls(habitat_id, name, url_image, description)


        except Exception as e:
            print(f"Erreur lors de la création d'un habitat : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def list_all_habitats(cls):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name, url_image, description, created_at, updated_at FROM habitats ORDER BY id")
            rows = cur.fetchall()
            habitats = []
            for row in rows:
                habitat = cls(*row)
                habitats.append(habitat)
            return habitats
        except Exception as e:
            print(f"Erreur lors de la récupération des habitats : {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def get_habitat_by_id(cls, habitat_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, name, url_image, description, created_at, updated_at
                FROM habitats WHERE id = %s
            """, (habitat_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération de l'habitat par id : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def update_habitat(cls, habitat_id, name, url_image, description):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE habitats
                SET name=%s, url_image=%s, description=%s, updated_at=NOW()
                WHERE id=%s
            """, (name, description, url_image, habitat_id))
            conn.commit()
            if cur.rowcount == 0:
                print(f"Aucun habitat trouvé avec l'id {habitat_id} pour mise à jour.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'habitat : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def delete_habitat(cls, habitat_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM habitats WHERE id = %s", (habitat_id,))
            conn.commit()
            if cur.rowcount == 0:
                print(f"Aucun habitat trouvé avec l'id {habitat_id} à supprimer.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'habitat : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

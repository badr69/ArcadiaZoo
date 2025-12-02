from app.db.psql import get_db_connection

class HabitatModel:
    """Modèle pour gérer les habitats."""

    def __init__(self, habitat_id, name, url_image, description, created_at=None, updated_at=None):
        self.habitat_id = habitat_id
        self.name = name
        self.url_image = url_image
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    # ===================== READ =====================
    @classmethod
    def list_all_habitats(cls):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT habitat_id, name, url_image, description, created_at, updated_at
                        FROM habitats
                        ORDER BY habitat_id
                    """)
                    rows = cur.fetchall()
                    return [cls(*row) for row in rows]
        except Exception as e:
            print(f"[list_all_habitats error]: {e}")
            return []

    @classmethod
    def get_habitat_by_id(cls, habitat_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT habitat_id, name, url_image, description, created_at, updated_at
                        FROM habitats
                        WHERE habitat_id = %s
                    """, (habitat_id,))
                    row = cur.fetchone()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"[get_habitat_by_id error]: {e}")
            return None

    # ===================== CREATE =====================
    @classmethod
    def create_habitat(cls, name, url_image, description):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT habitat_id FROM habitats WHERE name = %s", (name,))
                    if cur.fetchone():
                        print(f"[create_habitat warning]: Nom déjà existant: {name}")
                        return None

                    cur.execute("""
                        INSERT INTO habitats (name, url_image, description)
                        VALUES (%s, %s, %s)
                        RETURNING habitat_id, created_at
                    """, (name, url_image, description))
                    habitat_id, created_at = cur.fetchone()
                    conn.commit()
                    return cls(habitat_id, name, url_image, description, created_at)
        except Exception as e:
            print(f"[create_habitat error]: {e}")
            return None

    # ===================== UPDATE =====================
    def update_habitat(self, name, url_image, description):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT habitat_id FROM habitats 
                        WHERE name = %s AND habitat_id != %s
                    """, (name, self.habitat_id))
                    if cur.fetchone():
                        print(f"[update_habitat warning]: Nom déjà utilisé: {name}")
                        return False

                    cur.execute("""
                        UPDATE habitats
                        SET name = %s, url_image = %s, description = %s, updated_at=NOW()
                        WHERE habitat_id=%s
                    """, (name, url_image, description, self.habitat_id))
                    conn.commit()

                    self.name = name
                    self.url_image = url_image
                    self.description = description
                    return True
        except Exception as e:
            print(f"[update_habitat error]: {e}")
            return False

    # ===================== DELETE =====================
    def delete_habitat(self):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM habitats WHERE habitat_id = %s", (self.habitat_id,))
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"[delete_habitat error]: {e}")
            return False








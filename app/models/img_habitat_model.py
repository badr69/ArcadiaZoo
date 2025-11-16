from app.db.psql import get_db_connection

class ImgHabitatModel:
    """
    Modèle OOP représentant une image associée à un habitat.
    """

    def __init__(self, img_ha_id=None, habitat_id=None, filename=None,
                 description=None, created_at=None, updated_at=None):
        self.img_ha_id = img_ha_id
        self.habitat_id = habitat_id
        self.filename = filename
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    # -----------------------------
    # Classmethods : lecture / création
    # -----------------------------
    @classmethod
    def list_all_ha_img(cls):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, habitat_id, filename, description, created_at, updated_at "
                            "FROM img_habitats")
                rows = cur.fetchall()
                return [cls(*row) for row in rows]
        finally:
            conn.close()

    @classmethod
    def get_ha_img_by_id(cls, img_id: int) -> 'ImgHabitatModel':
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, habitat_id, filename, description, created_at, updated_at "
                            "FROM img_habitats WHERE id = %s", (img_id,))
                row = cur.fetchone()
                if not row:
                    raise LookupError(f"Image habitat avec id {img_id} introuvable")
                return cls(*row)
        finally:
            conn.close()

    @classmethod
    def create_ha_img(cls, habitat_id: int, filename: str, description: str) -> 'ImgHabitatModel':
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO img_habitats (habitat_id, filename, description) "
                    "VALUES (%s, %s, %s) RETURNING id",
                    (habitat_id, filename, description)
                )
                new_id = cur.fetchone()[0]
                conn.commit()
                return cls(new_id, habitat_id, filename, description)
        finally:
            conn.close()

    # -----------------------------
    # Méthodes d'instance : update / delete
    # -----------------------------
    def update_ha_img(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE img_habitats SET habitat_id = %s, filename = %s, description = %s WHERE id=%s",
                    (self.habitat_id, self.filename, self.description, self.img_ha_id)
                )
                conn.commit()
        finally:
            conn.close()

    def delete_ha_img(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM img_habitats WHERE id=%s", (self.img_ha_id,))
                conn.commit()
        finally:
            conn.close()

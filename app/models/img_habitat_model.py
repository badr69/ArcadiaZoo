from app.db.psql import get_db_connection


class ImgHabitat:
    def __init__(self, id=None, habitat_id=None, filename=None, description=None, created_at=None, updated_at=None):
        self.id = id
        self.habitat_id = habitat_id
        self.filename = filename
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def get_all() -> list['ImgHabitat']:
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, habitat_id, filename, description, created_at, updated_at FROM img_habitats")
                rows = cur.fetchall()
                return [ImgHabitat(*row) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(image_id: int) -> 'ImgHabitat':
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, habitat_id, filename, description, created_at, updated_at FROM img_habitats WHERE id = %s",
                    (image_id,))
                row = cur.fetchone()
                if not row:
                    raise LookupError(f"Image habitat with id {image_id} not found.")
                return ImgHabitat(*row)
        finally:
            conn.close()

    @staticmethod
    def create(habitat_id: int, filename: str, description: str) -> int:
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO img_habitats (habitat_id, filename, description)
                    VALUES (%s, %s, %s) RETURNING id
                """, (habitat_id, filename, description))
                new_id = cur.fetchone()[0]
                conn.commit()
                return new_id
        finally:
            conn.close()

    @staticmethod
    def update(image_id: int, habitat_id: int, filename: str, description: str) -> None:
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE img_habitats SET habitat_id=%s, filename=%s, description=%s WHERE id=%s",
                    (habitat_id, filename, description, image_id)
                )
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(image_id: int) -> None:
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM img_habitats WHERE id=%s", (image_id,))
                conn.commit()
        finally:
            conn.close()

from app.db.psql import get_db_connection

class AnimalModel:
    def __init__(self, id, name, race, url_image, habitat_id, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.race = race
        self.url_image = url_image
        self.habitat_id = habitat_id
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def list_all_animals(cls):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name, race, url_image, habitat_id, created_at, updated_at FROM animals ORDER BY id")
            rows = cur.fetchall()
            animals = [cls(*row) for row in rows]
            return animals
        except Exception as e:
            print(f"Erreur lors de la récupération des animaux : {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def get_animal_by_id(cls, animal_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, name, race, url_image, habitat_id, created_at, updated_at
                FROM animals
                WHERE id = %s
            """, (animal_id,))
            row = cur.fetchone()
            return cls(*row) if row else None
        except Exception as e:
            print(f"Erreur lors de la récupération de l'animal par ID : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def create_animal(cls, name, race, url_image, habitat_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO animals (name, race, url_image, habitat_id)
                VALUES (%s, %s, %s, %s) RETURNING id, created_at
            """, (name, race, url_image, habitat_id))
            animal_id, created_at = cur.fetchone()
            conn.commit()
            return cls(id=animal_id, name=name, race=race, url_image=url_image, habitat_id=habitat_id, created_at=created_at)
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[create_animal] Erreur : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def update_animal(cls, animal_id, name, race, url_image):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE animals
                SET name = %s,
                    race = %s,
                    url_images = %s,
                    updated_at = NOW()
                WHERE id = %s
            """, (animal_id, name, race, url_image, ))
            conn.commit()
            if cur.rowcount == 0:
                print(f"Aucun animal trouvé avec l'id {animal_id} pour mise à jour.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour de animal : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def delete_animal(cls, animal_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM animals WHERE id = %s", (animal_id,))
            conn.commit()
            if cur.rowcount == 0:
                print(f"Aucun animal trouvé avec l'id {animal_id} à supprimer.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'animal : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

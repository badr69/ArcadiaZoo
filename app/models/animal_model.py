from app.db.psql import get_db_connection


class AnimalModel:
    def __init__(self, id, name, url_image, description, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.url_image = url_image
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_animal(cls, name, url_image, description):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO animals (name, url_image, description)
                VALUES (%s, %s, %s)
                RETURNING id, created_at
            """, (name, url_image, description))
            row = cur.fetchone()
            print("Resultat RETURNING :", row)
            conn.commit()
            animal_id, created_at = row
            return cls(animal_id, name, url_image, description)

        except Exception as e:
            print(f"Erreur lors de la création d'un animals : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def list_all_animals(cls):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name, url_image, description, created_at, updated_at FROM animals ORDER BY id")
            rows = cur.fetchall()
            animals = []
            for row in rows:
                animal = cls(*row)
                animals.append(animal)
            return animals
        except Exception as e:
            print(f"Erreur lors de la récupération des animalss : {e}")
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
                SELECT id, name, url_image, description, created_at, updated_at
                FROM animals WHERE id = %s
            """, (animal_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération de l'animals par id : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def update_animal(cls, animals_id, name, url_image, description):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE animals
                SET name=%s, url_image=%s, description=%s, updated_at=NOW()
                WHERE id=%s
            """, (name, description, url_image, animals_id))
            conn.commit()
            if cur.rowcount == 0:
                print(f"Aucun animals trouvé avec l'id {animals_id} pour mise à jour.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'animals : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def delete_animal(cls, animals_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM animals WHERE id = %s", (animals_id,))
            conn.commit()
            if cur.rowcount == 0:
                print(f"Aucun animals trouvé avec l'id {animals_id} à supprimer.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'animals : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

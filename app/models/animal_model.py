from app.db.psql import get_db_connection


class AnimalModel:
    def __init__(self, animal_id, name, race, description, url_image, habitat_id, created_at=None, updated_at=None):
        self.animal_id = animal_id
        self.name = name
        self.race = race
        self.description = description
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
            cur.execute(
                "SELECT animal_id, name, race, description, url_image, habitat_id, created_at, updated_at FROM animals ORDER BY animal_id")
            rows = cur.fetchall()
            animals = []
            for row in rows:
                animals.append(cls(*row))
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
                        SELECT animal_id, name, race, description, url_image, habitat_id, created_at, updated_at
                        FROM animals
                        WHERE animal_id = %s
                        """, (animal_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération de l'animal par id : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def create_animal(cls, name, race, description, url_image, habitat_id):
        """Crée un nouvel animal et retourne l'objet créé"""
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO animals (name, race, description, url_image, habitat_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING animal_id, created_at
            """, (name, race, description, url_image, habitat_id))
            row = cur.fetchone()
            print("Resultat RETURNING :", row)
            conn.commit()
            animal_id, created_at = row
            # TODO: Ajouter created_at dans l'objet retourné pour avoir toutes les données
            return cls(animal_id, name, race, description, url_image, habitat_id, created_at)
        except Exception as e:
            print(f"Erreur lors de la création d'un animal : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def update(self):
        """Met à jour cet animal dans la base de données"""
        if not self.animal_id:
            print("Erreur : l'animal doit avoir un animal_id pour être mis à jour.")
            return False
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                        UPDATE animals
                        SET name = %s,
                            race = %s,
                            description = %s,
                            url_image = %s,
                            habitat_id = %s,
                            updated_at = NOW()
                        WHERE animal_id = %s
                        """, (self.name, self.race, self.description, self.url_image, self.habitat_id, self.animal_id))
            conn.commit()
            if cur.rowcount == 0:
                # TODO: le cas où l'animal n'existe pas (retourner message clair ou exception)
                print(f"Aucun animal trouvé avec l'id {self.animal_id} pour mise à jour.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'animal : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def delete(self):
        """Supprime cet animal de la base de données"""
        if not self.animal_id:
            print("Erreur : l'animal doit avoir un animal_id pour être supprimé.")
            return False
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM animals WHERE animal_id = %s", (self.animal_id,))
            conn.commit()
            if cur.rowcount == 0:
                # TODO le cas où l'animal à supprimer n'existe pas
                print(f"Aucun animal trouvé avec l'id {self.animal_id} à supprimer.")
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

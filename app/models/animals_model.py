from app.db.psql import get_db_connection




class AnimalModel:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    def get_all(self):
        try:
            self.cursor.execute("SELECT id, name, species FROM animals ORDER BY id")
            return self.cursor.fetchall()
        except Exception as e:
            print("Erreur get_all:", e)
            return []

    def get_by_id(self, animal_id):
        try:
            self.cursor.execute("SELECT id, name, species FROM animals WHERE id = %s", (animal_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print("Erreur get_by_id:", e)
            return None

    def create(self, name, species):
        try:
            self.cursor.execute("INSERT INTO animals (name, species) VALUES (%s, %s)", (name, species))
            self.conn.commit()
        except Exception as e:
            print("Erreur create:", e)
            self.conn.rollback()

    def update(self, animal_id, name, species):
        try:
            self.cursor.execute("UPDATE animals SET name = %s, species = %s WHERE id = %s", (name, species, animal_id))
            self.conn.commit()
        except Exception as e:
            print("Erreur update:", e)
            self.conn.rollback()

    def delete(self, animal_id):
        try:
            self.cursor.execute("DELETE FROM animals WHERE id = %s", (animal_id,))
            self.conn.commit()
        except Exception as e:
            print("Erreur delete:", e)
            self.conn.rollback()

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print("Erreur fermeture:", e)

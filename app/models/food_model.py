from app.db.psql import get_db_connection

class FoodModel:
    def __init__(self, animal_id, type_food, quantity, date_food, id=None):
        self.id = id
        self.animal_id = animal_id
        self.type_food = type_food
        self.quantity = quantity
        self.date_food = date_food


    @staticmethod
    def list_all_foods():
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT f.id, a.name AS animal_name, f.type_food, f.quantity, f.date_food
                FROM foods f
                JOIN animals a ON f.animal_id = a.id
                ORDER BY f.date_food DESC
            """)
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print("Erreur récupération:", e)
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_food_by_id(food_id):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id, animal_id, type_food, quantity, date_food
                FROM foods
                WHERE id = %s
            """, (food_id,))
            row = cur.fetchone()
            if row:
                return FoodModel(
                    id=row[0],
                    animal_id=row[1],
                    type_food=row[2],
                    quantity=row[3],
                    date_food=row[4]
                )
            return None
        except Exception as e:
            print("Erreur get_by_id:", e)
            return None
        finally:
            cur.close()
            conn.close()

    def create_food(self):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO foods (animal_id, type_food, quantity, date_food)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (self.animal_id, self.type_food, self.quantity, self.date_food))
            self.id = cur.fetchone()[0]
            conn.commit()
            return self.id
        except Exception as e:
            conn.rollback()
            print("Erreur création nourriture:", e)
            return None
        finally:
            cur.close()
            conn.close()

    def update_food(self):
        if self.id is None:
            print("Erreur : impossible de mettre à jour un objet sans id")
            return False

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE foods
                SET animal_id = %s,
                    type_food = %s,
                    quantity = %s,
                    date_food = %s,
                    updated_at = NOW()
                WHERE id = %s
            """, (self.animal_id, self.type_food, self.quantity, self.date_food, self.id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("Erreur mise à jour:", e)
            return False
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def delete_food(food_id):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM foods WHERE id = %s", (food_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("Erreur suppression:", e)
            return False
        finally:
            cur.close()
            conn.close()

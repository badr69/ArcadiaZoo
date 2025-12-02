from app.db.psql import get_db_connection
from datetime import datetime

class FoodModel:
    def __init__(self, food_id, animal_id, vet_id, employee_id,
                 name_food, quantity, date_food=None, created_at=None, updated_at=None):
        self.food_id = food_id
        self.animal_id = animal_id
        self.vet_id = vet_id
        self.employee_id = employee_id
        self.name_food = name_food
        self.quantity = quantity
        self.date_food = date_food
        self.created_at = created_at
        self.updated_at = updated_at

        # Conversion automatique des dates si strings
        self.date_food = (datetime.strptime(date_food, "%Y-%m-%d %H:%M:%S")
                          if isinstance(date_food, str) else date_food)
        self.created_at = (datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                           if isinstance(created_at, str) else created_at)
        self.updated_at = (datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
                           if isinstance(updated_at, str) else updated_at)


    # ===================== READ =====================
    @classmethod
    def list_all_foods(cls):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT food_id, animal_id, vet_id, employee_id,
                               name_food, quantity, date_food, created_at, updated_at
                        FROM foods
                        ORDER BY food_id
                    """)
                    rows = cur.fetchall()
                    return [cls(*row) for row in rows]
        except Exception as e:
            print(f"[FoodModel.list_all_foods] Error: {e}")
            return []

    @classmethod
    def get_food_by_id(cls, food_id):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT food_id, animal_id, vet_id, employee_id,
                               name_food, quantity, date_food, created_at, updated_at
                        FROM foods
                        WHERE food_id = %s
                    """, (food_id,))
                    row = cur.fetchone()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"[FoodModel.get_food_by_id] Error: {e}")
            return None

    # ===================== USERS =====================
    @classmethod
    def list_all_vets(cls):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT u.user_id, u.username
                        FROM users u
                        JOIN roles r ON u.role_id = r.role_id
                        WHERE r.name = 'vet'
                        ORDER BY u.username
                    """)
                    rows = cur.fetchall()
                    return [{"user_id": r[0], "username": r[1]} for r in rows]
        except Exception as e:
            print(f"[FoodModel.list_all_vets] Error: {e}")
            return []

    # ===================== CREATE =====================
    @classmethod
    def create_food(cls, animal_id, vet_id, employee_id, name_food, quantity, date_food=None):
        date_food = date_food or datetime.now()
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO foods (animal_id, vet_id, employee_id, name_food, quantity, date_food)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING food_id
                    """, (animal_id, vet_id, employee_id, name_food, quantity, date_food))
                    food_id = cur.fetchone()[0]
                    conn.commit()
                    return cls.get_food_by_id(food_id)
        except Exception as e:
            print(f"[FoodModel.create_food] Error: {e}")
            return None

    # ===================== UPDATE =====================
    def update_food(self, animal_id=None, vet_id=None, employee_id=None, name_food=None, quantity=None, date_food=None):
        animal_id = animal_id or self.animal_id
        vet_id = vet_id or self.vet_id
        employee_id = employee_id or self.employee_id
        name_food = name_food or self.name_food
        quantity = quantity or self.quantity
        date_food = date_food or self.date_food
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE foods
                        SET animal_id = %s,
                            vet_id = %s,
                            employee_id = %s,
                            name_food = %s,
                            quantity = %s,
                            date_food = %s,
                            updated_at = NOW()
                        WHERE food_id = %s
                    """, (animal_id, vet_id, employee_id, name_food, quantity, date_food, self.food_id))
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"[FoodModel.update_food] Error: {e}")
            return False

    # ===================== DELETE =====================
    def delete_food(self):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM foods WHERE food_id = %s", (self.food_id,))
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"[FoodModel.delete_food] Error: {e}")
            return False

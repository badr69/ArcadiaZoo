from app.models.food_model import FoodModel
from app.models.user_model import UserModel
from app.models.animal_model import AnimalModel
from app.utils.security import sanitize_html, detect_sql_injection
from datetime import datetime, timezone


class FoodService:

    # ===================== LISTING =====================
    @classmethod
    def list_all_foods(cls) -> list[FoodModel]:
        try:
            return FoodModel.list_all_foods()
        except Exception as e:
            print(f"[FoodService.list_all_foods] Error: {e}")
            return []

    @classmethod
    def list_all_vets(cls):
        try:
            return UserModel.list_all_vets()
        except Exception as e:
            print(f"[FoodService.list_all_vets] Error: {e}")
            return []

    @classmethod
    def list_all_employees(cls):
        try:
            return UserModel.list_all_employees()
        except Exception as e:
            print(f"[FoodService.list_all_employees] Error: {e}")
            return []

    # ===================== VALIDATION =====================
    @staticmethod
    def _sanitize_and_validate(animal_id, vet_id, employee_id, name_food, quantity):
        name_food = sanitize_html(name_food)
        if detect_sql_injection(name_food):
            raise ValueError("SQL injection détectée.")

        try:
            animal_id = int(animal_id)
            vet_id = int(vet_id)
            employee_id = int(employee_id) if employee_id else None
        except:
            raise ValueError("ID invalide (non numérique).")

        if animal_id <= 0 or vet_id <= 0 or (employee_id and employee_id <= 0):
            raise ValueError("ID doit être positif.")

        animal = AnimalModel.get_animal_by_id(animal_id)
        if not animal:
            raise ValueError("Animal inexistant.")

        vet = UserModel.get_user_by_id(vet_id)
        if not vet or vet.role_name != "vet":
            raise ValueError("Vétérinaire invalide.")

        if employee_id:
            employee = UserModel.get_user_by_id(employee_id)
            if not employee or employee.role_name != "employee":
                raise ValueError("Employé invalide.")

        try:
            quantity = float(quantity)
        except:
            raise ValueError("Quantité invalide.")
        if quantity <= 0:
            raise ValueError("La quantité doit être positive.")

        return animal_id, vet_id, employee_id, name_food, quantity

    # ===================== CREATE =====================
    @classmethod
    def create_food(cls, animal_id, vet_id, employee_id, name_food, quantity, date_food=None) -> FoodModel:
        animal_id, vet_id, employee_id, name_food, quantity = cls._sanitize_and_validate(
            animal_id, vet_id, employee_id, name_food, quantity
        )
        date_food = date_food or datetime.now(timezone.utc)
        return FoodModel.create_food(animal_id, vet_id, employee_id, name_food, quantity, date_food)

    # ===================== INSTANCE =====================
    def __init__(self, food_id):
        self.food = FoodModel.get_food_by_id(food_id)
        if not self.food:
            raise ValueError("Food inexistant.")

    def get_food_by_id(self) -> FoodModel:
        return self.food

    # ===================== UPDATE =====================
    def update_food(self, animal_id, vet_id, employee_id, name_food, quantity, date_food=None) -> FoodModel:
        if not self.food:
            raise ValueError("Food inexistant.")

        animal_id, vet_id, employee_id, name_food, quantity = self._sanitize_and_validate(
            animal_id, vet_id, employee_id, name_food, quantity
        )
        date_food = date_food or datetime.now(timezone.utc)

        success = self.food.update_food(animal_id, vet_id, employee_id, name_food, quantity, date_food)
        if not success:
            raise Exception("Erreur lors de la mise à jour du Food.")

        # Recharger l'objet mis à jour
        self.food = FoodModel.get_food_by_id(self.food.food_id)
        return self.food

    # ===================== DELETE =====================
    def delete_food(self) -> bool:
        if not self.food:
            raise ValueError("Food inexistant.")
        return self.food.delete_food()

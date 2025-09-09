from app.models.animal_click_model import AnimalClickModel

class AnimalClickService:

    @staticmethod
    def add_click(mongo_db, animal_id):
        AnimalClickModel.add_click(mongo_db["animal_clicks"], animal_id)

    @staticmethod
    def get_total_clicks(mongo_db, animal_id):
        return AnimalClickModel.get_total_clicks(mongo_db["animal_clicks"], animal_id)

    @staticmethod
    def get_clicks_by_date(mongo_db, animal_id):
        return AnimalClickModel.get_clicks_by_date(mongo_db["animal_clicks"], animal_id)

    @staticmethod
    def get_clicks_for_animal_id(mongo_db, animal_id):
        return AnimalClickModel.get_clicks_by_animal(mongo_db["animal_clicks"], animal_id)


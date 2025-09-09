from app.services.animal_click_service import AnimalClickService


class AnimalClickController:

    @staticmethod
    def add_click(animal_id):
        AnimalClickService.add_click(animal_id)
        return {"message": "Click added"}, 201

    @staticmethod
    def get_total_clicks(animal_id):
        total = AnimalClickService.get_total_clicks(animal_id)
        return {"animal_id": animal_id, "total_clicks": total}, 200

    @staticmethod
    def get_clicks_by_date(animal_id):
        data = AnimalClickService.get_clicks_by_date(animal_id)
        return {"animal_id": animal_id, "clicks_by_date": data}, 200

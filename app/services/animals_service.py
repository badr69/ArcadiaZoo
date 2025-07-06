from app.models.animal_model import AnimalModel

class AnimalService:

    @staticmethod
    def get_all_animals():
        model = AnimalModel()
        try:
            return model.get_all()
        except Exception as e:
            print("Erreur service get_all_animals:", e)
            return []
        finally:
            model.close()

    @staticmethod
    def get_animal_by_id(animal_id):
        model = AnimalModel()
        try:
            return model.get_by_id(animal_id)
        except Exception as e:
            print("Erreur service get_animal_by_id:", e)
            return None
        finally:
            model.close()

    @staticmethod
    def create_animal(name, species):
        model = AnimalModel()
        try:
            model.create(name, species)
            return True
        except Exception as e:
            print("Erreur service create_animal:", e)
            return False
        finally:
            model.close()

    @staticmethod
    def update_animal(animal_id, name, species):
        model = AnimalModel()
        try:
            model.update(animal_id, name, species)
            return True
        except Exception as e:
            print("Erreur service update_animal:", e)
            return False
        finally:
            model.close()

    @staticmethod
    def delete_animal(animal_id):
        model = AnimalModel()
        try:
            model.delete(animal_id)
            return True
        except Exception as e:
            print("Erreur service delete_animal:", e)
            return False
        finally:
            model.close()

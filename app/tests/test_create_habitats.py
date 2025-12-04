import unittest
from app.models.habitat_model import HabitatModel
from app.db.psql import get_db_connection

class TestHabitat(unittest.TestCase):
    def setUp(self):
        self.name = "Jungle Africaine"
        self.url_image = "uploads/habitats/jungle.jpg"
        self.description = "Habitat pour animaux tropicaux"

        # Supprime tout habitat avec le même nom avant le test (éviter doublons)
        self._delete_habitat_by_name(self.name)

    def test_create_habitat(self):
        habitat = HabitatModel.create_habitat(self.name, self.url_image, self.description)

        self.assertIsNotNone(habitat)
        self.assertEqual(habitat.name, self.name)
        self.assertEqual(habitat.url_image, self.url_image)
        self.assertEqual(habitat.description, self.description)
        self.assertIsNotNone(habitat.habitat_id)
        self.assertIsNotNone(habitat.created_at)

    def tearDown(self):
        # Supprime l’habitat créé après chaque test
        self._delete_habitat_by_name(self.name)

    def _delete_habitat_by_name(self, name):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM habitats WHERE name = %s", (name,))
            conn.commit()
        finally:
            cur.close()
            conn.close()

if __name__ == '__main__':
    unittest.main()

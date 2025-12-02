# app/models/animal_model.py
from app.db.psql import get_db_connection
from typing import List, Optional

class AnimalModel:
    """Modèle pour gérer les animaux."""

    def __init__(
        self,
        animal_id: int,
        name: str,
        race: str,
        description: str,
        url_image: str,
        habitat_id: int,
        habitat_name: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.animal_id = animal_id
        self.name = name
        self.race = race
        self.description = description
        self.url_image = url_image
        self.habitat_id = habitat_id
        self.habitat_name = habitat_name
        self.created_at = created_at
        self.updated_at = updated_at

    # ===================== READ =====================
    @classmethod
    def list_all_animals(cls) -> List["AnimalModel"]:
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT a.animal_id,
                               a.name,
                               a.race,
                               a.description,
                               a.url_image,
                               a.habitat_id,
                               h.name AS habitat_name,
                               a.created_at,
                               a.updated_at
                        FROM animals a
                        LEFT JOIN habitats h ON a.habitat_id = h.habitat_id
                        ORDER BY a.animal_id
                    """)
                    rows = cur.fetchall()
                    return [cls(*row) for row in rows]
        except Exception as e:
            print(f"[list_all_animals error]: {e}")
            return []

    @classmethod
    def get_animal_by_id(cls, animal_id: int) -> Optional["AnimalModel"]:
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT a.animal_id,
                               a.name,
                               a.race,
                               a.description,
                               a.url_image,
                               a.habitat_id,
                               h.name AS habitat_name,
                               a.created_at,
                               a.updated_at
                        FROM animals a
                        LEFT JOIN habitats h ON a.habitat_id = h.habitat_id
                        WHERE a.animal_id = %s
                    """, (animal_id,))
                    row = cur.fetchone()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"[get_animal_by_id error]: {e}")
            return None

    # ===================== CREATE =====================
    @classmethod
    def create_animal(
        cls,
        name: str,
        race: str,
        description: str,
        url_image: str,
        habitat_id: int
    ) -> Optional["AnimalModel"]:
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT animal_id FROM animals WHERE name = %s", (name,))
                    if cur.fetchone():
                        print(f"[create_animal warning]: Nom déjà existant: {name}")
                        return None

                    cur.execute("""
                        INSERT INTO animals (name, race, description, url_image, habitat_id)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING animal_id, created_at
                    """, (name, race, description, url_image, habitat_id))
                    animal_id, created_at = cur.fetchone()
                    conn.commit()
                    return cls(animal_id, name, race, description, url_image, habitat_id, created_at=created_at)
        except Exception as e:
            print(f"[create_animal error]: {e}")
            return None

    # ===================== UPDATE =====================
    def update_animal(
        self,
        name: str,
        race: str,
        description: str,
        url_image: str,
        habitat_id: int
    ) -> bool:
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT animal_id FROM animals 
                        WHERE name = %s AND animal_id != %s
                    """, (name, self.animal_id))
                    if cur.fetchone():
                        print(f"[update_animal warning]: Nom déjà utilisé: {name}")
                        return False

                    cur.execute("""
                        UPDATE animals
                        SET name = %s, race = %s, description = %s, url_image = %s, habitat_id = %s, updated_at = NOW()
                        WHERE animal_id = %s
                    """, (name, race, description, url_image, habitat_id, self.animal_id))
                    conn.commit()

                    self.name = name
                    self.race = race
                    self.description = description
                    self.url_image = url_image
                    self.habitat_id = habitat_id
                    return True
        except Exception as e:
            print(f"[update_animal error]: {e}")
            return False

    # ===================== DELETE =====================
    def delete_animal(self) -> bool:
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM animals WHERE animal_id = %s", (self.animal_id,))
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            print(f"[delete_animal error]: {e}")
            return False


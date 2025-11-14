from app.db.psql import get_db_connection

class HabitatModel:
    """
    Modèle pour gérer les habitats.
    """

    def __init__(self, habitat_id, name, url_image, description, created_at=None, updated_at=None):
        self.habitat_id = habitat_id
        self.name = name
        self.url_image = url_image
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def id(self):
        return self.habitat_id

    # ===================== READ =====================
    @classmethod
    def list_all_habitats(cls):
        """
        Retourne tous les habitats de la base.
        TODO: ajouter pagination si la table devient trop grande.
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT habitat_id, name, url_image, description, created_at, updated_at
                        FROM habitats
                        ORDER BY habitat_id
                    """)
                    rows = cur.fetchall()
                    return [cls(*row) for row in rows]
        except Exception as e:
            print(f"[list_all_habitats error]: {e}")
            return []

    @classmethod
    def get_habitat_by_id(cls, habitat_id):
        """
        Retourne un habitat par son ID.
        TODO: lever une exception si l'habitat n'existe pas pour la gestion côté service.
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT habitat_id, name, url_image, description, created_at, updated_at
                        FROM habitats
                        WHERE habitat_id = %s
                    """, (habitat_id,))
                    row = cur.fetchone()
                    return cls(*row) if row else None
        except Exception as e:
            print(f"[get_habitat_by_id error]: {e}")
            return None

    # ===================== CREATE =====================
    @classmethod
    def create_habitat(cls, name, url_image, description):
        """
        Crée un nouvel habitat et le retourne.
        TODO:
        - Vérifier l'unicité du nom avant insertion.
        - Ajouter validation des données (ex: nom non vide, url valide).
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    # Vérification d'unicité (TODO: améliorer en renvoyant message si existant)
                    cur.execute("SELECT habitat_id FROM habitats WHERE name = %s", (name,))
                    if cur.fetchone():
                        print(f"[create_habitat warning]: Nom d'habitat déjà existant: {name}")
                        return None

                    cur.execute("""
                        INSERT INTO habitats (name, url_image, description)
                        VALUES (%s, %s, %s)
                        RETURNING habitat_id, created_at
                    """, (name, url_image, description))
                    row = cur.fetchone()
                    conn.commit()
                    habitat_id, created_at = row
                    return cls(habitat_id, name, url_image, description, created_at)
        except Exception as e:
            print(f"[create_habitat error]: {e}")
            return None

    # ===================== UPDATE =====================
    def update_habitat(self, name, url_image, description):
        """
        Met à jour les informations de cet habitat.
        TODO:
        - Vérifier si le nouveau nom existe déjà pour un autre habitat.
        - Ajouter validation des données (ex: url valide, longueur du nom).
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    # Vérification unicité du nom pour autre habitat
                    cur.execute("""
                        SELECT habitat_id FROM habitats 
                        WHERE name = %s AND habitat_id != %s
                    """, (name, self.habitat_id))
                    if cur.fetchone():
                        print(f"[update_habitat warning]: Nom d'habitat déjà utilisé: {name}")
                        return False

                    cur.execute("""
                        UPDATE habitats
                        SET name = %s,
                            url_image = %s,
                            description = %s,
                            updated_at = NOW()
                        WHERE habitat_id = %s
                    """, (name, url_image, description, self.habitat_id))

                    if cur.rowcount == 0:
                        # TODO: gérer le cas où l'habitat n'existe pas
                        print(f"[update_habitat warning]: Aucun habitat trouvé avec l'id {self.habitat_id}")
                        return False

                    conn.commit()
                    # Mise à jour des attributs de l'objet en mémoire
                    self.name = name
                    self.url_image = url_image
                    self.description = description
                    return True
        except Exception as e:
            print(f"[update_habitat error]: {e}")
            return False

    # ===================== DELETE =====================
    def delete_habitat(self):
        """
        Supprime cet habitat de la base.
        TODO:
        - Vérifier dépendances (ex: animaux liés à cet habitat) avant suppression.
        - Retourner message clair si suppression impossible.
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM habitats WHERE habitat_id = %s", (self.habitat_id,))
                    conn.commit()
                    if cur.rowcount == 0:
                        # TODO: gérer le cas où l'habitat n'existe pas
                        print(f"[delete_habitat warning]: Aucun habitat trouvé avec l'id {self.habitat_id}")
                        return False
                    return True
        except Exception as e:
            print(f"[delete_habitat error]: {e}")
            return False

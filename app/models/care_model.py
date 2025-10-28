from app.db.psql import get_db_connection
from datetime import datetime


class CareModel:
    def __init__(self, id, animal_id, user_id, type_care, description, date_care=None,
                 created_at=None, updated_at=None):
        self.id = id
        self.animal_id = animal_id
        self.user_id = user_id
        self.type_care = type_care
        self.description = description
        self.date_care = date_care
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def list_all_cares(cls):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                        SELECT id,
                               animal_id,
                               user_id,
                               type_care,
                               description,
                               date_care,
                               created_at,
                               updated_at
                        FROM cares
                        ORDER BY date_care DESC
                        """)
            rows = cur.fetchall()
            cares = []
            for row in rows:
                cares.append(cls(*row))
            return cares
        except Exception as e:
            print(f"Erreur lors de la récupération des soins : {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @classmethod
    def get_care_by_id(cls, care_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                        SELECT id,
                               animal_id,
                               user_id,
                               type_care,
                               description,
                               date_care,
                               created_at,
                               updated_at
                        FROM cares
                        WHERE id = %s
                        """, (care_id,))
            row = cur.fetchone()
            if row:
                return cls(*row)
            return None
        except Exception as e:
            print(f"Erreur lors de la récupération du soin par id : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def create_care(animal_id, user_id, type_care, description, date_care=None):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                        INSERT INTO cares (animal_id, user_id, type_care, description, date_care)
                        VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at, updated_at
                        """, (animal_id, user_id, type_care, description, date_care or datetime.now()))
            row = cur.fetchone()
            conn.commit()
            care_id, created_at, updated_at = row
            return CareModel(care_id, animal_id, user_id, type_care, description, date_care, created_at, updated_at)
        except Exception as e:
            print(f"Erreur lors de la création d'un soin : {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def update_care(care_id, animal_id, user_id, type_care, description, date_care=None):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                        UPDATE cares
                        SET animal_id=%s,
                            user_id=%s,
                            type_care=%s,
                            description=%s,
                            date_care=%s,
                            updated_at=NOW()
                        WHERE id = %s
                        """, (animal_id, user_id, type_care, description, date_care or datetime.now(), care_id))
            conn.commit()
            if cur.rowcount == 0:
                print(f"Aucun soin trouvé avec l'id {care_id} pour mise à jour.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour du soin : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def delete_care(care_id):
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM cares WHERE id = %s", (care_id,))
            conn.commit()
            if cur.rowcount == 0:
                print(f"Aucun soin trouvé avec l'id {care_id} à supprimer.")
                return False
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression du soin : {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

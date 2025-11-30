from app.db.psql import get_db_connection
from datetime import datetime


class CareModel:
    """
    Modèle représentant un soin (care) dans le zoo.
    Correspond à la table 'cares' dans PostgreSQL.
    """

    def __init__(self, care_id, animal_id, user_id, type_care, description,
                 date_care=None, created_at=None, updated_at=None):

        self.care_id = care_id
        self.animal_id = animal_id
        self.user_id = user_id
        self.type_care = type_care
        self.description = description

        # Conversion automatique des dates si strings
        self.date_care = (datetime.strptime(date_care, "%Y-%m-%d %H:%M:%S")
                          if isinstance(date_care, str) else date_care)
        self.created_at = (datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                           if isinstance(created_at, str) else created_at)
        self.updated_at = (datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
                           if isinstance(updated_at, str) else updated_at)

    # ======================================================
    # LIST ALL CARES
    # ======================================================
    @classmethod
    def list_all_cares(cls):
        """
        Retourne tous les soins triés par date décroissante.
        Retour : liste d’objets CareModel
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                                SELECT care_id,
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
                    return [cls(*row) for row in rows]

        except Exception as e:
            print(f"Erreur list_all_cares : {e}")
            return []

    # ======================================================
    # GET CARE BY ID
    # ======================================================
    @classmethod
    def get_care_by_id(cls, care_id):
        """
        Retourne un soin par son ID.
        Retour : CareModel ou None
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                                SELECT care_id,
                                       animal_id,
                                       user_id,
                                       type_care,
                                       description,
                                       date_care,
                                       created_at,
                                       updated_at
                                FROM cares
                                WHERE care_id = %s
                                """, (care_id,))
                    row = cur.fetchone()

                    return cls(*row) if row else None

        except Exception as e:
            print(f"Erreur get_care_by_id : {e}")
            return None

    # ======================================================
    # CREATE CARE
    # ======================================================
    @classmethod
    def create_care(cls, animal_id, user_id, type_care, description, date_care=None):
        """
        Crée un nouveau soin.
        Retour : objet CareModel ou None
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                                INSERT INTO cares (animal_id, user_id, type_care, description, date_care)
                                VALUES (%s, %s, %s, %s, %s)
                                RETURNING care_id, created_at, updated_at
                                """, (animal_id, user_id, type_care, description,
                                      date_care or datetime.now()))

                    care_id, created_at, updated_at = cur.fetchone()
                    return cls(care_id, animal_id, user_id, type_care, description,
                               date_care, created_at, updated_at)

        except Exception as e:
            print(f"Erreur create_care : {e}")
            return None

    # ======================================================
    # UPDATE CARE
    # ======================================================
    def update_care(self, animal_id, user_id, type_care, description, date_care=None):
        """
        Met à jour le soin actuel.
        Retour : True si succès, False sinon.
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                                UPDATE cares
                                SET animal_id   = %s,
                                    user_id     = %s,
                                    type_care   = %s,
                                    description = %s,
                                    date_care   = %s,
                                    updated_at  = NOW()
                                WHERE care_id = %s
                                """, (animal_id, user_id, type_care, description,
                                      date_care or datetime.now(), self.care_id))

                    return cur.rowcount > 0

        except Exception as e:
            print(f"Erreur update_care : {e}")
            return False

    # ======================================================
    # DELETE CARE
    # ======================================================
    def delete_care(self):
        """
        Supprime le soin actuel.
        Retour : True si succès, False sinon.
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                                DELETE
                                FROM cares
                                WHERE care_id = %s
                                """, (self.care_id,))
                    return cur.rowcount > 0

        except Exception as e:
            print(f"Erreur delete_care : {e}")
            return False

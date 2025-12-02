# from app.db.psql import get_db_connection
# from datetime import datetime
#
# class ImgHabitatModel:
#     """
#     Modèle représentant une image associée à un habitat.
#     """
#     def __init__(self, img_ha_id, habitat_id, filename, description,
#                  created_at=None, updated_at=None):
#         self.img_ha_id = img_ha_id
#         self.habitat_id = habitat_id
#         self.filename = filename
#         self.description = description
#         self.created_at = created_at
#         self.updated_at = updated_at
#
#     # ===================== LIST =====================
#     @classmethod
#     def list_all_img_ha(cls):
#         try:
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute("""
#                         SELECT img_ha_id, habitat_id, filename, description, created_at, updated_at
#                         FROM img_habitats
#                         ORDER BY img_ha_id
#                     """)
#                     rows = cur.fetchall()
#                     return [cls(*row) for row in rows]
#         except Exception as e:
#             print(f"[ImgHabitatModel.list_all_img_habitat] Error: {e}")
#             return []
#
#     # ===================== GET BY ID =====================
#     @classmethod
#     def get_img_ha_by_id(cls, img_ha_id):
#         try:
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute("""
#                         SELECT img_ha_id, habitat_id, filename, description, created_at, updated_at
#                         FROM img_habitats
#                         WHERE img_ha_id = %s
#                     """, (img_ha_id,))
#                     row = cur.fetchone()
#                     return cls(*row) if row else None
#         except Exception as e:
#             print(f"[ImgHabitatModel.get_img_ha_by_id] Error: {e}")
#             return None
#
#     # ===================== CREATE =====================
#     @classmethod
#     def create_img_habitat(cls, habitat_id, filename, description):
#         try:
#             created_at = datetime.now()
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute("""
#                         INSERT INTO img_habitats (habitat_id, filename, description, created_at)
#                         VALUES (%s, %s, %s, %s)
#                         RETURNING img_ha_id
#                     """, (habitat_id, filename, description, created_at))
#                     img_ha_id = cur.fetchone()[0]
#                     conn.commit()
#                     return cls.get_img_ha_by_id(img_ha_id)
#         except Exception as e:
#             print(f"[ImgHabitatModel.create_img_habitat] Error: {e}")
#             return None
#
#     # ===================== UPDATE =====================
#     def update_img_habitat(self, habitat_id, filename, description):
#         try:
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute("""
#                         UPDATE img_habitats
#                         SET habitat_id = %s,
#                             filename   = %s,
#                             description = %s,
#                             updated_at = NOW()
#                         WHERE img_ha_id = %s
#                     """, (habitat_id, filename, description, self.img_ha_id))
#                     conn.commit()
#                     return cur.rowcount > 0
#         except Exception as e:
#             print(f"[ImgHabitatModel.update_img_habitat] Error: {e}")
#             return False
#
#     # ===================== DELETE =====================
#     def delete_img_habitat(self):
#         try:
#             with get_db_connection() as conn:
#                 with conn.cursor() as cur:
#                     cur.execute("DELETE FROM img_habitats WHERE img_ha_id = %s", (self.img_ha_id,))
#                     conn.commit()
#                     return cur.rowcount > 0
#         except Exception as e:
#             print(f"[ImgHabitatModel.delete_img_habitat] Error: {e}")
#             return False

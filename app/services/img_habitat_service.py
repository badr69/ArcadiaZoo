import os
from flask import current_app
from werkzeug.utils import secure_filename
from app.models.img_habitat_model import ImgHabitatModel

class ImgHabitatService:
    """Service métier pour les images d'habitats."""

    @classmethod
    def list_all_ha_img(cls):
        return ImgHabitatModel.list_all_ha_img()

    @classmethod
    def get_ha_img_by_id(cls, img_id: int) -> ImgHabitatModel:
        return ImgHabitatModel.get_ha_img_by_id(img_id)

    @classmethod
    def create_ha_img(cls, habitat_id: int, image_file, description: str = "") -> ImgHabitatModel:
        if not image_file or image_file.filename == '':
            raise ValueError("Aucun fichier reçu pour l'image")

        filename = secure_filename(image_file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        if ext not in current_app.config['ALLOWED_EXTENSIONS']:
            raise ValueError("Extension de fichier non autorisée")

        upload_folder = current_app.config['HABITAT_IMG_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        image_file.save(file_path)

        url_image = f"uploads/habitat_img/{filename}"
        return ImgHabitatModel.create_ha_img(habitat_id, url_image, description)

    @classmethod
    def update_ha_img(cls, img_id: int, habitat_id: int, image_file=None, description: str = None) -> ImgHabitatModel:
        img = ImgHabitatModel.get_ha_img_by_id(img_id)

        # Upload nouvelle image si fournie
        if image_file and hasattr(image_file, 'filename') and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            if ext not in current_app.config['ALLOWED_EXTENSIONS']:
                raise ValueError("Extension de fichier non autorisée")

            old_path = os.path.join(current_app.config['HABITAT_IMG_FOLDER'], os.path.basename(img.filename))
            if os.path.exists(old_path):
                os.remove(old_path)

            new_path = os.path.join(current_app.config['HABITAT_IMG_FOLDER'], filename)
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            image_file.save(new_path)
            img.filename = f"uploads/habitat_img/{filename}"

        img.habitat_id = habitat_id
        if description is not None:
            img.description = description

        # Appel de la méthode d'instance update()
        img.update()
        return ImgHabitatModel.get_ha_img_by_id(img_id)

    @classmethod
    def delete(cls, img_id: int) -> bool:
        img = ImgHabitatModel.get_ha_img_by_id(img_id)
        file_path = os.path.join(current_app.config['HABITAT_IMG_FOLDER'], os.path.basename(img.filename))
        if os.path.exists(file_path):
            os.remove(file_path)
        img.delete()
        return True

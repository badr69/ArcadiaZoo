import os
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    ext = filename.rsplit('.', 1)[-1].lower()
    return '.' in filename and ext in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_image(file, subfolder):
    """Sauvegarde un fichier dans un sous-dossier (ex: animal_img)"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        folder_path = current_app.config[subfolder]
        file_path = os.path.join(folder_path, filename)
        file.save(file_path)
        # Retourne le chemin relatif à "static"
        return f"uploads/{subfolder.split('_')[0]}_img/{filename}"
    return None

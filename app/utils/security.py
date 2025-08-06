import re
import secrets
import bleach
from typing import Dict, List
from werkzeug.security import generate_password_hash, check_password_hash



def hash_password(password: str) -> str:
    # Hash avec un salt et un algorithme sécurisé (pbkdf2:sha256 par défaut)
    return generate_password_hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    # Vérifie si le mot de passe correspond au hash
    return check_password_hash(hashed_password, password)

def generate_token(length: int = 32) -> str:
    # Génère un token hexadécimal sécurisé
    return secrets.token_hex(length)

def sanitize_html(input_str: str) -> str:
    """
    Nettoie une chaîne HTML pour éviter les injections XSS.
    Autorise uniquement les tags et attributs basiques sûrs.
    """
    allowed_tags: List[str] = [
        'b', 'i', 'u', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li'
    ]
    allowed_attrs: Dict[str, List[str]] = {
        'a': ['href', 'title', 'target', 'rel']  # Ajouté 'rel' pour sécurité sur les liens
    }

    cleaned = bleach.clean(
        input_str,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )
    return cleaned

def detect_sql_injection(input_str: str) -> bool:
    """
    Détecte des motifs simples pouvant indiquer une injection SQL.
    Retourne True si un motif suspect est trouvé, False sinon.
    """
    pattern = re.compile(
        r"(--|;|'|\"|/\*|\*/|\b(SELECT|UPDATE|DELETE|INSERT|DROP|ALTER|CREATE|EXEC|UNION|XP_)\b)",
        re.IGNORECASE
    )
    return bool(pattern.search(input_str))

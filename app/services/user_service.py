from app.models.user_model import UserModel

class UserService:
    """Service pour gérer la logique métier des utilisateurs."""

    def list_all_users(self):
        """Retourne la liste de tous les utilisateurs."""
        return UserModel.list_all_users()

    def get_user_by_id(self, user_id):
        """Retourne un utilisateur par son ID."""
        return UserModel.get_user_by_id(user_id)

    def get_user_by_email(self, email):
        """Retourne un utilisateur par son email."""
        return UserModel.get_user_by_email(email)

    def create_user(self, username, email, password, role_id=None):
        """Crée un utilisateur avec règles métier.

        - Vérifie si l'email existe déjà.
        - Définit un rôle par défaut si role_id non fourni.
        """
        # Vérifier si l'email est déjà utilisé
        if UserModel.get_user_by_email(email):
            return None, "Cet email est déjà utilisé."

        # Définir un rôle par défaut si aucun fourni
        if role_id is None:
            role_id = 2  # par exemple 2 = utilisateur standard

        # Créer l'utilisateur via le modèle
        user = UserModel.create_user(username, email, password, role_id)
        if not user:
            return None, "Erreur lors de la création de l'utilisateur."

        return user, "Utilisateur créé avec succès."

    def update_user(self, user, username=None, email=None, role_id=None):
        """Met à jour un utilisateur avec logique métier.

        - Vérifie si l'email n'est pas déjà utilisé par un autre.
        """
        # Vérifier email existant pour un autre utilisateur
        if email and email != user.email:
            existing_user = UserModel.get_user_by_email(email)
            if existing_user and existing_user.user_id != user.user_id:
                return {"error": "Cet email est déjà utilisé par un autre utilisateur."}, 400

        # Appeler la méthode de mise à jour du modèle
        return user.update_user(username=username, email=email, role_id=role_id)

    def delete_user(self, user):
        """Supprime un utilisateur avec logique métier.

        - On peut ajouter des règles supplémentaires ici si nécessaire,
          par exemple empêcher la suppression d'un admin principal.
        """
        return user.delete_user()

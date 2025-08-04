ArcadiaZoo

Arcadia est un zoo situé en France près de la forêt de Brocéliande, en Bretagne depuis 1960.
Ils possèdent tout un panel d’animaux, répartis par habitat (savane, jungle, marais) et font extrêmement attention à leur santé.

-requirements.txt
python-dotenv~=1.1.0
Flask~=3.1.1
pip~=25.1
Jinja2~=3.1.6
MarkupSafe~=3.0.2
Werkzeug~=3.1.3
click~=8.2.1
blinker~=1.9.0
itsdangerous~=2.2.0
gunicorn~=23.0.0
flask_wtf~=1.2.2
psycopg2~=2.9.10
pymongo~=4.13.2
Flask_Login~=0.6.3
bleach==6.1.0


instalation
- Ubuntu 22.04
- PostgreSQL (psycopg2-binary)
- pgadmin
- MongoDB (pymongo)
- PyCharm (IDE)

Étapes

1. Cloner le dépôt :
   git clone https://github.com/badr69/ArcadiaZoo
   cd ArcadiaZoo

2. Créer et activer un environnement virtuel :
   python3 -m venv .venv
   source .venv/bin/activate

3. Installer les dépendances :
   pip install -r requirements.txt

4. Configurer la base de données PostgreSQL et MongoDB (ajouter les paramètres dans un fichier .env)

5. Lancer l’application :
   flask run

6. Ouvrir dans le navigateur :
   http://localhost:5000

7. Pour docker, j'utiliserai render pour le deploiement et il ne necessite le docker.
je ferais une procedure apart.

---

Fonctionnalités principales

- Gestion des utilisateurs, animaux et habitats
- Gestion des soins et suivi de la santé des animaux
- Gestion des visiteurs
- Authentification sécurisée des utilisateurs
- Utilisation conjointe de PostgreSQL et MongoDB pour les données

---

.
├── app
├── config.py
│   ├── controllers
│   │   ├── animal_controller.py
│   │   ├── auth_controller.py
│   │   ├── habitat_controller.py
│   │   ├── __pycache__
│   │   ├── review_controller.py
│   │   ├── role_controller.py
│   │   ├── service_controller.py
│   │   └── user_controller.py
│   ├── dash_app
│   ├── db
│   │   ├── mongo.py
│   │   ├── psql.py
│   │   └── __pycache__
│   ├── extensions
│   │   ├── __init__.py
│   │   ├── login_manager.py
│   │   └── __pycache__
│   ├── forms
│   │   ├── animal_forms.py
│   │   ├── auth_forms.py
│   │   ├── contact_forms.py
│   │   ├── habitat_comment_forms.py
│   │   ├── habitat_forms.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── report_forms.py
│   │   ├── review_form.py
│   │   ├── service_forms.py
│   │   ├── upload_image_forms.py
│   │   └── user_forms.py
│   ├── __init__.py
│   ├── models
│   │   ├── animal_model.py
│   │   ├── habitat_model.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── review_model.py
│   │   ├── role_model.py
│   │   ├── service_model.py
│   │   └── user_model.py
│   ├── __pycache__
│   │   ├── config.cpython-312.pyc
│   │   └── __init__.cpython-312.pyc
│   ├── routes
│   │   ├── admin_route.py
│   │   ├── animal_routes.py
│   │   ├── auth_routes.py
│   │   ├── employee_route.py
│   │   ├── habitats_routes.py
│   │   ├── __init__.py
│   │   ├── main_routes.py
│   │   ├── __pycache__
│   │   ├── review_route.py
│   │   ├── role_routes.py
│   │   ├── service_routes.py
│   │   ├── user_routes.py
│   │   └── vet_route.py
│   ├── services
│   │   ├── animal_service.py
│   │   ├── habitat_service.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── review_service.py
│   │   ├── role_service.py
│   │   ├── service_service.py
│   │   └── user_service.py
│   ├── static
│   │   ├── css
│   │   ├── images
│   │   ├── js
│   │   └── uploads
│   ├── templates
│   │   ├── animal
│   │   ├── animals.html
│   │   ├── auth
│   │   ├── base.html
│   │   ├── contact.html
│   │   ├── dash
│   │   ├── habitat
│   │   ├── habitats.html
│   │   ├── index.html
│   │   ├── navbar.html
│   │   ├── role
│   │   ├── service
│   │   ├── services.html
│   │   ├── user
│   │   └── user_detail.html
│   ├── tests
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── test_create_habitats.py
│   │   └── test_demo.py
│   └── utils
│       ├── allowedfiles.py
│       ├── image_upload.py
│       ├── __init__.py
│       ├── __pycache__
│       ├── security.py
│       └── validator.py
├── badr.txt
├── docker
│   ├── docker-compose.yml
│   └── Dockerfile
├── main.py
├── __pycache__
├── Readme.md
├── requirements.txt
├── schema.sql
├── test_mongo.py
├── test_postgres.py
└── test_review_insert.py

37 directories, 78 files



Contribuer


Merci de créer une branche dédiée, tester vos modifications, puis faire une pull request.



Contact

Derrouiche badreddine – manoudb@yahoo.fr
Lien GitHub : https://github.com/badr69/ArcadiaZoo



Made with ❤️ by derrouiche Badreddine


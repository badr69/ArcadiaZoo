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
je ferais une procedure apart. render ne se connecte pas au bdd meme avec les bon parametres, j'essaye de trouver des solutions.
8. sur la branch features/docker, j'ai nstaller docker depuis le site officiel de docker.
j'ai Dockerfile et docker-compose et j'ai ajoute au requirements,
l'application fonctionne avec docker.
---

Fonctionnalités principales

- Gestion des utilisateurs, animaux et habitats
- Gestion des soins et suivi de la santé des animaux
- Gestion des visiteurs
- Authentification sécurisée des utilisateurs
- Utilisation conjointe de PostgreSQL et MongoDB pour les données

---

├── app
│   ├── config.py
│   ├── controllers
│   │   ├── animal_controller.py
│   │   ├── auth_controller.py
│   │   ├── habitat_controller.py
│   │   ├── review_controller.py
│   │   ├── role_controller.py
│   │   ├── service_controller.py
│   │   └── user_controller.py
│   ├── db
│   │   ├── mongo.py
│   │   └── psql.py
│   ├── extensions
│   │   ├── __init__.py
│   │   └── login_manager.py
│   ├── forms
│   │   ├── animal_forms.py
│   │   ├── auth_forms.py
│   │   ├── contact_forms.py
│   │   ├── habitat_comment_forms.py
│   │   ├── habitat_forms.py
│   │   ├── __init__.py
│   │   ├── report_forms.py
│   │   ├── review_form.py
│   │   ├── service_forms.py
│   │   ├── upload_image_forms.py
│   │   └── user_forms.py
│   ├── __init__.py
│   ├── models
│   │   ├── animal_model.py
│   │   ├── habitat_model.py
│   │   ├── __init__.py
│   │   ├── review_model.py
│   │   ├── role_model.py
│   │   ├── service_model.py
│   │   └── user_model.py
│   ├── routes
│   │   ├── admin_route.py
│   │   ├── animal_routes.py
│   │   ├── auth_routes.py
│   │   ├── employee_route.py
│   │   ├── habitats_routes.py
│   │   ├── __init__.py
│   │   ├── main_routes.py
│   │   ├── review_route.py
│   │   ├── role_routes.py
│   │   ├── service_routes.py
│   │   ├── user_routes.py
│   │   └── vet_route.py
│   ├── services
│   │   ├── animal_service.py
│   │   ├── habitat_service.py
│   │   ├── __init__.py
│   │   ├── review_service.py
│   │   ├── role_service.py
│   │   ├── service_service.py
│   │   └── user_service.py
│   ├── static
│   │   ├── css
│   │   │   ├── dash.css
│   │   │   └── styles.css
│   │   ├── images
│   │   │   ├── figma
│   │   │   │   ├── Capture d’écran du 2024-11-21 20-24-07.png
│   │   │   │   ├── Capture d’écran du 2024-11-21 20-25-17.png
│   │   │   │   ├── Capture d’écran du 2024-11-21 20-25-55.png
│   │   │   │   └── Capture d’écran du 2024-11-21 20-27-07.png
│   │   │   ├── header.jpg
│   │   │   ├── imagesAnimaux
│   │   │   │   ├── Babouin.jpeg
│   │   │   │   ├── canard.jpeg
│   │   │   │   ├── Elephant.jpeg
│   │   │   │   ├── Flament Rose.jpeg
│   │   │   │   ├── giraffe.jpeg
│   │   │   │   ├── Grand heron.jpeg
│   │   │   │   ├── jaguar.jpeg
│   │   │   │   ├── leopard.jpeg
│   │   │   │   ├── lion.jpeg
│   │   │   │   ├── perroquet.jpeg
│   │   │   │   └── zebre.jpeg
│   │   │   ├── imagesHabitats
│   │   │   │   ├── jungle.png
│   │   │   │   ├── marais.jpeg
│   │   │   │   └── Savane.png
│   │   │   ├── imagesServices
│   │   │   │   ├── restaurant.jpg
│   │   │   │   └── train.jpg
│   │   │   ├── Safari.jpeg
│   │   │   └── Schemas
│   │   │       ├── Flowchart Template - Cadre 1.jpg
│   │   │       ├── Flowchart Template - Cadre 2.jpg
│   │   │       └── schéma de donnée.jpg
│   │   ├── js
│   │   │   ├── login.js
│   │   │   ├── review_1.js
│   │   │   └── review.js
│   │   └── uploads
│   │       ├── animal_img
│   │       │   ├── Babouin.jpeg
│   │       │   ├── canard.jpeg
│   │       │   ├── Elephant.jpeg
│   │       │   ├── Flament_Rose.jpeg
│   │       │   ├── giraffe.jpeg
│   │       │   ├── jaguar.jpeg
│   │       │   ├── leopard.jpeg
│   │       │   └── lion.jpeg
│   │       ├── habitat_img
│   │       │   ├── header.jpg
│   │       │   ├── jungle.png
│   │       │   ├── marais.jpeg
│   │       │   ├── Safari.jpeg
│   │       │   └── Savane.png
│   │       ├── jungle.png
│   │       ├── lion.jpeg
│   │       ├── marais.jpeg
│   │       ├── Savane.png
│   │       └── service_img
│   │           ├── restaurant.jpg
│   │           └── train.jpg
│   ├── templates
│   │   ├── animal
│   │   │   ├── animal_detail.html
│   │   │   ├── animal_details.html
│   │   │   ├── create_animal.html
│   │   │   ├── list_all_animals.html
│   │   │   └── update_animal.html
│   │   ├── animals.html
│   │   ├── auth
│   │   │   ├── login.html
│   │   │   └── logout.html
│   │   ├── base_dashboard.html
│   │   ├── base.html
│   │   ├── contact.html
│   │   ├── dash
│   │   │   ├── admin_dash.html
│   │   │   ├── employee_dash.html
│   │   │   └── vet_dash.html
│   │   ├── footer.html
│   │   ├── habitat
│   │   │   ├── create_habitat.html
│   │   │   ├── habitat_details.html
│   │   │   ├── list_all_habitats.html
│   │   │   └── update_habitat.html
│   │   ├── habitats.html
│   │   ├── index.html
│   │   ├── navbar.html
│   │   ├── role
│   │   │   ├── __init__.py
│   │   │   └── list_all_roles.html
│   │   ├── service
│   │   │   ├── create_service.html
│   │   │   ├── list_all_services.html
│   │   │   ├── service_details.html
│   │   │   └── update_service.html
│   │   ├── services.html
│   │   ├── sidebar.html
│   │   ├── user
│   │   │   ├── create_user.html
│   │   │   ├── list_all_users.html
│   │   │   ├── update_user.html
│   │   │   └── user_detail.html
│   │   └── user_detail.html
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_create_habitats.py
│   │   └── test_demo.py
│   └── utils
│       ├── allowedfiles.py
│       ├── decorators.py
│       ├── image_upload.py
│       ├── __init__.py
│       ├── security.py
│       └── validator.py
├── badr.txt
├── docker
│   ├── docker-compose.yml
│   └── Dockerfile
├── main.py
├── readme.md
├── requirements.txt
├── schema.sql
├── test_collection.py
├── test_get.py
├── test_mongo.py
├── test_postgres.py
└── test_review_insert.py


Merci de créer une branche dédiée, tester vos modifications, puis faire une pull request.


Contact
Derrouiche badreddine – manoudb@yahoo.fr
Lien GitHub : https://github.com/badr69/ArcadiaZoo

Made with ❤️ by derrouiche Badreddine


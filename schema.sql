-- creation table roles
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- creation table users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- augmenter la taille pour hash
    role_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- creation table habitats
CREATE TABLE IF NOT EXISTS habitats (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    url_image VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- creation table img_habitats
CREATE TABLE IF NOT EXISTS img_habitats (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table d'association (habitats et img_habitats)=habitats_images
CREATE TABLE IF NOT EXISTS habitats_images (
    habitat_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    PRIMARY KEY (habitat_id, image_id),
    FOREIGN KEY (habitat_id) REFERENCES habitats(id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES img_habitats(id) ON DELETE CASCADE
);

-- creation table animals
CREATE TABLE IF NOT EXISTS animals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    race VARCHAR(100) NOT NULL,
    url_image VARCHAR(255),
    habitat_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (habitat_id) REFERENCES habitats(id) ON DELETE SET NULL
);

-- creation table img_animaux
CREATE TABLE IF NOT EXISTS img_animals (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table d'association (animaux et img_animals)= animals_images
CREATE TABLE IF NOT EXISTS animals_images (
    animal_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    PRIMARY KEY (animal_id, image_id),
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES img_animals(id) ON DELETE CASCADE
);

-- creation table services
CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    url_image VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- creation table img_services
CREATE TABLE IF NOT EXISTS img_services (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table d'association (services et img_services)= services_images
CREATE TABLE IF NOT EXISTS services_images (
    service_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    PRIMARY KEY (service_id, image_id),
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES img_services(id) ON DELETE CASCADE
);

-- creation table nourriture
CREATE TABLE IF NOT EXISTS foods (
    id SERIAL PRIMARY KEY,
    animal_id INTEGER NOT NULL,
    type_nourriture VARCHAR(100) NOT NULL,
    quantite VARCHAR(50) NOT NULL,
    date_nourriture TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE
);

-- creation table care
CREATE TABLE IF NOT EXISTS care (
    id SERIAL PRIMARY KEY,
    animal_id INTEGER NOT NULL,
    user_id INTEGER,
    type_soin VARCHAR(100) NOT NULL,
    description TEXT,
    date_soin TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- creation table report_vet
CREATE TABLE IF NOT EXISTS report_vet (
    id SERIAL PRIMARY KEY,
    animal_id INTEGER NOT NULL,
    user_id INTEGER,
    state VARCHAR(100) NOT NULL,
    food VARCHAR(100) NOT NULL,
    quantity_food VARCHAR(100) NOT NULL,
    description_state TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Fonction commune pour tous les triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP AT TIME ZONE 'UTC';
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- triggers
-- Trigger pour la table users
CREATE TRIGGER trg_update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger pour la table habitats
CREATE TRIGGER trg_update_habitats_updated_at
BEFORE UPDATE ON habitats
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger pour la table img_habitats
CREATE TRIGGER trg_update_img_habitats_updated_at
BEFORE UPDATE ON img_habitats
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger pour la table animaux
CREATE TRIGGER trg_update_animals_updated_at
BEFORE UPDATE ON animals
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger pour la table img_animaux
CREATE TRIGGER trg_update_img_animals_updated_at
BEFORE UPDATE ON img_animals
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger pour la table services
CREATE TRIGGER trg_update_services_updated_at
BEFORE UPDATE ON services
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger pour la table img_services
CREATE TRIGGER trg_update_img_services_updated_at
BEFORE UPDATE ON img_services
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger pour la table nourritures
CREATE TRIGGER trg_update_foods_updated_at
BEFORE UPDATE ON foods
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger pour la table soins
CREATE TRIGGER trg_update_care_updated_at
BEFORE UPDATE ON care
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger pour la table report_vet
CREATE TRIGGER trg_update_report_vet_updated_at
BEFORE UPDATE ON report_vet
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


-- Création des rôles une seule fois (admin, employee, vet):
INSERT INTO roles (name)
VALUES
    ('admin'),
    ('employee'),
    ('vet')
ON CONFLICT (name) DO NOTHING;

-- Récupérer l'id du rôle 'admin'
SELECT id FROM roles WHERE name = 'admin';


-- Insértion de l'utilisateur admin (exécution après avoir vérifié l'id)
INSERT INTO users (username, email, password, role_id)
VALUES (
  'badreddine',
  'manoudb@yahoo.fr',
  'scrypt:32768:8:1$AkHoEIrDx2ZvfEAR$27abaead494269f6a60b9b42cf307216085cd6bde45f8d6e989017db663c9dbf316a1bd3ddba747c9054047fb2e504ff21c51122dcac9f355dcc50c09fc5a2ee',
  1
)
ON CONFLICT (email) DO NOTHING;


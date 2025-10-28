-- Table roles
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- Table habitats
CREATE TABLE IF NOT EXISTS habitats (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    url_image VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table images habitats
CREATE TABLE IF NOT EXISTS img_habitats (
    id SERIAL PRIMARY KEY,
    habitat_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (habitat_id) REFERENCES habitats(id) ON DELETE CASCADE
);

-- Table animals
CREATE TABLE IF NOT EXISTS animals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    race VARCHAR(100) NOT NULL,
    description TEXT,
    url_image VARCHAR(255),
    habitat_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (habitat_id) REFERENCES habitats(id) ON DELETE SET NULL
);

-- Table images animals
CREATE TABLE IF NOT EXISTS img_animals (
    id SERIAL PRIMARY KEY,
    animal_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE
);

-- Table services
CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    url_image VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table images services
CREATE TABLE IF NOT EXISTS img_services (
    id SERIAL PRIMARY KEY,
    service_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
);

-- Table foods
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

-- Table care (soins)
CREATE TABLE IF NOT EXISTS cares (
    id SERIAL PRIMARY KEY,
    animal_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    type_care VARCHAR(100) NOT NULL,
    description TEXT,
    date_care TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Table report_vet
CREATE TABLE IF NOT EXISTS report_vet (
    id SERIAL PRIMARY KEY,
    animal_id INTEGER NOT NULL,
    user_id INTEGER,
    care_id INTEGER,
    state VARCHAR(100) NOT NULL,
    food VARCHAR(100) NOT NULL,
    quantity_food VARCHAR(100) NOT NULL,
    description_state TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (care_id) REFERENCES cares(id) ON DELETE SET NULL
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
-- Trigger pour la table roless
CREATE TRIGGER trg_update_roles_updated_at
BEFORE UPDATE ON roles
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

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


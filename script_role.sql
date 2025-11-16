
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

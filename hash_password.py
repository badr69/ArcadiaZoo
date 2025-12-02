from werkzeug.security import generate_password_hash

hashed_password = generate_password_hash("Setif_19000")
print(hashed_password)

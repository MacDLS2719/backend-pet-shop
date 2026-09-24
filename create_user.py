import bcrypt
from app.database import SessionLocal
from app.models import Usuario

def create_admin_user():
    db = SessionLocal()
    
    username = "admin"
    email = "admin@petshop.com"
    raw_password = "123"
    
    # 1. Verificar si el usuario ya existe
    existing_user = db.query(Usuario).filter(
        (Usuario.username == username) | (Usuario.email == email)
    ).first()

    if existing_user:
        print(f"⚠️ El usuario '{username}' o email '{email}' ya existe en la base de datos.")
        db.close()
        return

    # 2. Hash directo con bcrypt
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
    hashed_str = hashed_bytes.decode('utf-8')

    # 3. Mapeo exacto con app/models.py
    new_user = Usuario(
        username=username,
        email=email,
        hashed_password=hashed_str,
        activo=True
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print("--------------------------------------------------")
        print("✅ ¡Usuario administrador insertado en Supabase!")
        print(f"👤 Username: {new_user.username}")
        print(f"📧 Email: {new_user.email}")
        print(f"🔑 Contraseña: {raw_password}")
        print("--------------------------------------------------")
    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear el usuario: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
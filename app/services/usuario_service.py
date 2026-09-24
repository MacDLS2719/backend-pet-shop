from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas
import bcrypt

# 1. Crear Usuario
def crear_usuario(db: Session, usuario_data: schemas.UsuarioCreate):
    # Validar si ya existe el usuario o email
    if db.query(models.Usuario).filter(models.Usuario.username == usuario_data.username).first():
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    
    nuevo_usuario = models.Usuario(
        username=usuario_data.username,
        email=usuario_data.email,
        hashed_password=usuario_data.password,  # Contraseña directa
        activo=True
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# 2. Listar todos los usuarios
def obtener_usuarios(db: Session):
    return db.query(models.Usuario).all()

# 3. Editar Usuario
def actualizar_usuario(db: Session, usuario_id: int, datos: schemas.UsuarioUpdate):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if datos.username:
        usuario.username = datos.username
    if datos.email:
        usuario.email = datos.email
    if datos.password:
        usuario.hashed_password = datos.password
    if datos.activo is not None:
        usuario.activo = datos.activo

    db.commit()
    db.refresh(usuario)
    return usuario

# 4. Eliminar Usuario
def eliminar_usuario(db: Session, usuario_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"mensaje": f"Usuario {usuario_id} eliminado exitosamente"}

# 5. Login Sencillo (con bcrypt) - acepta username O email
def login_usuario(db: Session, login_data: schemas.LoginRequest):
    # Buscar por username O por email
    usuario = db.query(models.Usuario).filter(
        (models.Usuario.username == login_data.username) |
        (models.Usuario.email == login_data.username)
    ).first()

    if not usuario:
        print(f"[LOGIN] Usuario NO encontrado en DB")
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    print(f"[LOGIN] Usuario encontrado: {usuario.username}")
    print(f"[LOGIN] Hash en DB: {usuario.hashed_password[:40]}...")

    # Detectar si el hash es bcrypt o texto plano
    es_bcrypt = usuario.hashed_password.startswith("$2b$") or usuario.hashed_password.startswith("$2a$")
    print(f"[LOGIN] Es hash bcrypt: {es_bcrypt}")

    if es_bcrypt:
        password_valid = bcrypt.checkpw(
            login_data.password.encode('utf-8'),
            usuario.hashed_password.encode('utf-8')
        )
    else:
        # Contraseña en texto plano (usuarios creados sin bcrypt)
        password_valid = (login_data.password == usuario.hashed_password)

    print(f"[LOGIN] Password valida: {password_valid}")

    if not password_valid:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    return {"mensaje": "Login exitoso", "usuario": usuario}
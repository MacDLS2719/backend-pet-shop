from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import schemas
from app.services import usuario_service

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

# ⚠️ Login PRIMERO - antes de rutas dinámicas
@router.post("/login", response_model=schemas.LoginResponse)
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    return usuario_service.login_usuario(db, credentials)

# Registrar usuario
@router.post("", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_service.crear_usuario(db, usuario)

# Listar usuarios
@router.get("", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_service.obtener_usuarios(db)

# Editar usuario
@router.put("/{usuario_id}", response_model=schemas.UsuarioResponse)
def actualizar_usuario(usuario_id: int, datos: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    return usuario_service.actualizar_usuario(db, usuario_id, datos)

# Eliminar usuario
@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return usuario_service.eliminar_usuario(db, usuario_id)
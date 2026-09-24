from pydantic import BaseModel, EmailStr
from typing import Optional

# --- USUARIO ---
class UsuarioCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    activo: Optional[bool] = None

class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: str
    activo: bool

    class Config:
        from_attributes = True

# --- LOGIN ---
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    mensaje: str
    usuario: UsuarioResponse
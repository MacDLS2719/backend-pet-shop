from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date


# ==========================================
# 0. ESQUEMAS DE TIPO PERRO
# ==========================================

class TipoPerroBase(BaseModel):
    tipo: str
    tiempo_ducha: int

class TipoPerroCreate(TipoPerroBase):
    pass

class TipoPerroResponse(TipoPerroBase):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# 1. ESQUEMAS DE PROPIETARIO
# ==========================================

class PropietarioBase(BaseModel):
    nombre: str
    cedula: str
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    acepta_politicas: Optional[bool] = False

class PropietarioCreate(PropietarioBase):
    pass

class PropietarioResponse(PropietarioBase):
    id: int
    acepta_politicas: bool = False

    class Config:
        from_attributes = True


# ==========================================
# 2. ESQUEMAS DE MASCOTA
# ==========================================

class MascotaBase(BaseModel):
    nombre_mascota: str
    especie: str  # Ej: Perro, Gato, Conejo, Ave
    raza: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    edad: Optional[int] = None
    peso: Optional[float] = None
    color: Optional[str] = None
    genero: Optional[str] = None
    vacunas: Optional[bool] = False
    esterilizacion: Optional[bool] = False
    temperamento: Optional[str] = None
    id_foto: Optional[str] = None
    tipo_perro_id: Optional[int] = None
    tiene_pulgas: Optional[bool] = False  # Importante: retornado en la respuesta

class MascotaCreate(MascotaBase):
    propietario_id: Optional[int] = None
    propietario: Optional[PropietarioCreate] = None

class MascotaUpdate(BaseModel):
    nombre_mascota: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    edad: Optional[int] = None
    peso: Optional[float] = None
    color: Optional[str] = None
    genero: Optional[str] = None
    vacunas: Optional[bool] = None
    esterilizacion: Optional[bool] = None
    temperamento: Optional[str] = None
    id_foto: Optional[str] = None
    tipo_perro_id: Optional[int] = None
    tiene_pulgas: bool = False
    propietario_id: Optional[int] = None

class MascotaResponse(MascotaBase):
    id: int
    propietario_id: int
    propietario: PropietarioResponse
    tipo_perro: Optional[TipoPerroResponse] = None

    class Config:
        from_attributes = True
from pydantic import BaseModel
from datetime import date, time
from typing import List, Optional

# Schema para TipoServicio
class TipoServicioSchema(BaseModel):
    id: int
    tipo: str
    valor: float

    class Config:
        from_attributes = True

# Schema para la Mascota asociada
class MascotaSchema(BaseModel):
    id: int
    nombre_mascota: str
    especie: str
    raza: Optional[str] = None
    tiene_pulgas: bool

    class Config:
        from_attributes = True

class AgendamientoCreate(BaseModel):
    mascota_id: int
    servicios_ids: List[int]
    fecha: date
    hora_inicio: time
    transporte: Optional[bool] = False
    observaciones: Optional[str] = None

class AgendamientoResponse(BaseModel):
    id: int
    fecha: date
    hora_inicio: time
    hora_final: Optional[time] = None
    duracion: Optional[int] = None
    precio_total: Optional[float] = None
    transporte: Optional[bool] = False
    observaciones: Optional[str] = None
    tiene_pulgas: Optional[bool] = False
    estado: str
    mascota_id: int
    propietario_id: int
    
    # Inclusión de relaciones completas
    mascota: Optional[MascotaSchema] = None
    servicios: List[TipoServicioSchema] = []

    class Config:
        from_attributes = True
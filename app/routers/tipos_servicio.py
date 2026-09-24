from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app import models

router = APIRouter(prefix="/api/tipos-servicio", tags=["Tipos Servicio"])

class TipoServicioCreate(BaseModel):
    tipo: str
    valor: float

class TipoServicioResponse(BaseModel):
    id: int
    tipo: str
    valor: float
    class Config:
        from_attributes = True

@router.get("/", response_model=List[TipoServicioResponse])
def listar_tipos_servicio(db: Session = Depends(get_db)):
    return db.query(models.TipoServicio).all()

@router.post("/", response_model=TipoServicioResponse, status_code=status.HTTP_201_CREATED)
def crear_tipo_servicio(datos: TipoServicioCreate, db: Session = Depends(get_db)):
    nuevo = models.TipoServicio(tipo=datos.tipo, valor=datos.valor)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

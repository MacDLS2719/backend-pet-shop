from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models
from app.schemas_pkg.mascota_schema import TipoPerroCreate, TipoPerroResponse

router = APIRouter(prefix="/api/tipos-perro", tags=["Tipos Perro"])

@router.get("/", response_model=List[TipoPerroResponse])
def obtener_tipos_perro(db: Session = Depends(get_db)):
    return db.query(models.TipoPerro).all()

@router.post("/", response_model=TipoPerroResponse, status_code=status.HTTP_201_CREATED)
def crear_tipo_perro(datos: TipoPerroCreate, db: Session = Depends(get_db)):
    nuevo_tipo = models.TipoPerro(**datos.model_dump())
    db.add(nuevo_tipo)
    db.commit()
    db.refresh(nuevo_tipo)
    return nuevo_tipo

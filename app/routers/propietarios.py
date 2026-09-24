from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models
from app.schemas_pkg.mascota_schema import PropietarioResponse, PropietarioCreate

router = APIRouter(prefix="/api/propietarios", tags=["Propietarios"])

@router.get("/", response_model=List[PropietarioResponse])
def obtener_propietarios(db: Session = Depends(get_db)):
    return db.query(models.Propietario).all()

@router.post("/", response_model=PropietarioResponse, status_code=status.HTTP_201_CREATED)
def crear_propietario(datos: PropietarioCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe por cédula
    existente = db.query(models.Propietario).filter(models.Propietario.cedula == datos.cedula).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un propietario con esa cédula.")
    
    nuevo_propietario = models.Propietario(**datos.model_dump())
    db.add(nuevo_propietario)
    db.commit()
    db.refresh(nuevo_propietario)
    return nuevo_propietario

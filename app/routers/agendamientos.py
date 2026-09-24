from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app import models
from app.schemas_pkg.agendamiento import AgendamientoCreate, AgendamientoResponse
from app.services import agendamiento_service

router = APIRouter(prefix="/api/agendamientos", tags=["Agendamientos"])

@router.get("/", response_model=List[AgendamientoResponse])
def listar_agendamientos(db: Session = Depends(get_db)):
    return db.query(models.Agendamiento)\
             .options(joinedload(models.Agendamiento.servicios), joinedload(models.Agendamiento.mascota))\
             .all()

@router.post("/", response_model=AgendamientoResponse)
def crear(data: AgendamientoCreate, db: Session = Depends(get_db)):
    return agendamiento_service.crear_nuevo_agendamiento(db, data)

@router.patch("/{id}/estado")
def cambiar_estado(id: int, nuevo_estado: str, observaciones: str = None, db: Session = Depends(get_db)):
    agendamiento = db.query(models.Agendamiento).filter(models.Agendamiento.id == id).first()
    if not agendamiento:
        raise HTTPException(status_code=404, detail="Agendamiento no encontrado.")
    
    agendamiento.estado = nuevo_estado
    if observaciones is not None:
        agendamiento.observaciones = observaciones
    
    # Regla: Al finalizar, si la mascota tenía pulgas, se limpia en la base de datos
    if nuevo_estado == "Completado":
        mascota = db.query(models.Mascota).filter(models.Mascota.id == agendamiento.mascota_id).first()
        if mascota and mascota.tiene_pulgas:
            mascota.tiene_pulgas = False
            
    db.commit()
    db.refresh(agendamiento)
    return agendamiento
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models
from app.schemas_pkg.mascota_schema import (
    MascotaCreate,
    MascotaUpdate,
    MascotaResponse
)

router = APIRouter(prefix="/api/mascotas", tags=["Mascotas"])

# 1. LISTAR MASCOTAS (Para alimentar las tarjetas del frontend)
@router.get("/", response_model=List[MascotaResponse])
def obtener_mascotas(db: Session = Depends(get_db)):
    return db.query(models.Mascota).all()

# 2. OBTENER DETALLE DE UNA MASCOTA
@router.get("/{mascota_id}", response_model=MascotaResponse)
def obtener_mascota_por_id(mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota

# 3. CREAR NUEVA MASCOTA (Crea o asocia el Propietario)
@router.post("/", response_model=MascotaResponse, status_code=status.HTTP_201_CREATED)
def crear_mascota(datos: MascotaCreate, db: Session = Depends(get_db)):
    target_propietario_id = datos.propietario_id

    # Si no nos envían un propietario_id, procesamos la información del nuevo propietario
    if not target_propietario_id:
        if not datos.propietario:
            raise HTTPException(
                status_code=400,
                detail="Se debe proporcionar un 'propietario_id' existente o la información del nuevo 'propietario'."
            )
        
        # Verificar si la cédula ya existe en la base de datos
        existente = db.query(models.Propietario).filter(
            models.Propietario.cedula == datos.propietario.cedula
        ).first()

        if existente:
            target_propietario_id = existente.id
        else:
            nuevo_propietario = models.Propietario(**datos.propietario.model_dump())
            db.add(nuevo_propietario)
            db.commit()
            db.refresh(nuevo_propietario)
            target_propietario_id = nuevo_propietario.id

    # Crear la mascota vinculando el ID del propietario
    dict_mascota = datos.model_dump(exclude={"propietario", "propietario_id"})
    nueva_mascota = models.Mascota(**dict_mascota, propietario_id=target_propietario_id)

    db.add(nueva_mascota)
    db.commit()
    db.refresh(nueva_mascota)
    return nueva_mascota

# 4. EDITAR MASCOTA
@router.put("/{mascota_id}", response_model=MascotaResponse)
def editar_mascota(mascota_id: int, datos: MascotaUpdate, db: Session = Depends(get_db)):
    mascota = db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    datos_actualizar = datos.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizar.items():
        setattr(mascota, clave, valor)

    db.commit()
    db.refresh(mascota)
    return mascota

# 5. ELIMINAR MASCOTA
@router.delete("/{mascota_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mascota(mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    db.delete(mascota)
    db.commit()
    return None
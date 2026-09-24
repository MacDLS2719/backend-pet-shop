from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Agendamiento, Mascota, TipoServicio, TipoPerro
from app.schemas_pkg.agendamiento import AgendamientoCreate

def crear_nuevo_agendamiento(db: Session, data: AgendamientoCreate):
    # 1. Obtener Mascota
    mascota = db.query(Mascota).filter(Mascota.id == data.mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="La mascota seleccionada no existe.")

    # 2. Calcular tiempo_ducha según TipoPerro
    duracion = 30  # Valor base si no se especifica
    if mascota.tipo_perro_id:
        tipo_perro = db.query(TipoPerro).filter(TipoPerro.id == mascota.tipo_perro_id).first()
        if tipo_perro and tipo_perro.tiempo_ducha:
            duracion = tipo_perro.tiempo_ducha

    # 3. Regla de Pulgas: Si la mascota tiene pulgas, agendar 2 días después
    fecha_agenda = data.fecha
    tiene_pulgas_flag = mascota.tiene_pulgas
    if tiene_pulgas_flag:
        fecha_agenda = data.fecha + timedelta(days=2)

    # 4. Calcular Hora Final
    inicio_datetime = datetime.combine(fecha_agenda, data.hora_inicio)
    fin_datetime = inicio_datetime + timedelta(minutes=duracion)
    hora_final = fin_datetime.time()

    # 5. Validar Disponibilidad de Horario (Evitar cruces)
    cruce = db.query(Agendamiento).filter(
        Agendamiento.fecha == fecha_agenda,
        Agendamiento.estado.in_(["Agendado", "En Proceso"]),
        Agendamiento.hora_inicio < hora_final,
        Agendamiento.hora_final > data.hora_inicio
    ).first()

    if cruce:
        raise HTTPException(
            status_code=400,
            detail=f"El horario de {data.hora_inicio.strftime('%H:%M')} a {hora_final.strftime('%H:%M')} ya está ocupado en la fecha {fecha_agenda}."
        )

    # 6. Calcular Precio Total
    servicios = db.query(TipoServicio).filter(TipoServicio.id.in_(data.servicios_ids)).all()
    precio_total = sum(s.valor for s in servicios)

    # 7. Crear el registro
    nuevo_agendamiento = Agendamiento(
        fecha=fecha_agenda,
        hora_inicio=data.hora_inicio,
        hora_final=hora_final,
        duracion=duracion,
        precio_total=precio_total,
        transporte=data.transporte,
        observaciones=data.observaciones,
        tiene_pulgas=tiene_pulgas_flag,
        estado="Agendado",
        propietario_id=mascota.propietario_id,
        mascota_id=mascota.id,
        servicios=servicios
    )

    db.add(nuevo_agendamiento)
    db.commit()
    db.refresh(nuevo_agendamiento)
    return nuevo_agendamiento


def cambiar_estado_servicio(db: Session, agendamiento_id: int, nuevo_estado: str):
    agendamiento = db.query(Agendamiento).filter(Agendamiento.id == agendamiento_id).first()
    if not agendamiento:
        raise HTTPException(status_code=404, detail="Agendamiento no encontrado.")

    agendamiento.estado = nuevo_estado

    # Regla: Al finalizar ("Completado"), si la mascota tenía pulgas, se le quitan
    if nuevo_estado == "Completado":
        mascota = db.query(Mascota).filter(Mascota.id == agendamiento.mascota_id).first()
        if mascota and mascota.tiene_pulgas:
            mascota.tiene_pulgas = False

    db.commit()
    return agendamiento
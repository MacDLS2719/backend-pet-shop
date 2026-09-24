from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Time, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from app.database import Base

# Tabla intermedia para la relación Muchos a Muchos entre Agendamiento y TipoServicio
agendamiento_servicios = Table(
    'agendamiento_servicios',
    Base.metadata,
    Column('agendamiento_id', Integer, ForeignKey('agendamientos.id'), primary_key=True),
    Column('tipo_servicio_id', Integer, ForeignKey('tipos_servicio.id'), primary_key=True)
)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    activo = Column(Boolean, default=True)


class Propietario(Base):
    __tablename__ = "propietarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    cedula = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String)
    email = Column(String, unique=True)
    direccion = Column(String)
    acepta_politicas = Column(Boolean, default=False, nullable=False)

    # Relaciones
    mascotas = relationship("Mascota", back_populates="propietario")
    agendamientos = relationship("Agendamiento", back_populates="propietario")


class TipoPerro(Base):
    __tablename__ = "tipos_perro"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)  # Ej: Pequeño, Mediano, Grande, Pelo Largo
    tiempo_ducha = Column(Integer, nullable=False)  # En minutos

    # Relación
    mascotas = relationship("Mascota", back_populates="tipo_perro")


class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    id_foto = Column(String, nullable=True)
    nombre_mascota = Column(String, nullable=False)
    especie = Column(String, nullable=False)  # Perro, Gato, etc.
    raza = Column(String)
    fecha_nacimiento = Column(Date)
    edad = Column(Integer)
    peso = Column(Float)
    color = Column(String)
    genero = Column(String)
    vacunas = Column(Boolean, default=False)
    esterilizacion = Column(Boolean, default=False)
    temperamento = Column(String)
    tiene_pulgas = Column(Boolean, default=False)

    # Claves foráneas
    propietario_id = Column(Integer, ForeignKey("propietarios.id"), nullable=False)
    tipo_perro_id = Column(Integer, ForeignKey("tipos_perro.id"), nullable=True)

    # Relaciones
    propietario = relationship("Propietario", back_populates="mascotas")
    tipo_perro = relationship("TipoPerro", back_populates="mascotas")
    agendamientos = relationship("Agendamiento", back_populates="mascota")


class TipoServicio(Base):
    __tablename__ = "tipos_servicio"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)  # Ej: Baño, Corte, Desparasitación
    valor = Column(Float, nullable=False)


class Agendamiento(Base):
    __tablename__ = "agendamientos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_final = Column(Time, nullable=False)
    duracion = Column(Integer)  # En minutos
    precio_total = Column(Float, nullable=False)
    transporte = Column(Boolean, default=False)
    observaciones = Column(String, nullable=True)
    tiene_pulgas = Column(Boolean, default=False)
    
    # Campo para control del flujo de la cita
    estado = Column(String, default="Agendado", nullable=False)  # Agendado, En Proceso, Completado, Cancelado

    # Claves foráneas
    propietario_id = Column(Integer, ForeignKey("propietarios.id"), nullable=False)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"), nullable=False)

    # Relaciones
    propietario = relationship("Propietario", back_populates="agendamientos")
    mascota = relationship("Mascota", back_populates="agendamientos")
    servicios = relationship("TipoServicio", secondary=agendamiento_servicios)
    
    # Relación uno a uno con el Feedback
    feedback = relationship("Feedback", back_populates="agendamiento", uselist=False)


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    calificacion = Column(Integer, nullable=False)  # Calificación del 1 al 5
    comentario = Column(Text, nullable=True)

    # Clave foránea única (Relación 1 a 1 con Agendamiento)
    agendamiento_id = Column(Integer, ForeignKey("agendamientos.id"), unique=True, nullable=False)

    # Relación inversa
    agendamiento = relationship("Agendamiento", back_populates="feedback")
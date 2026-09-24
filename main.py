from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app import models
from app.routers import usuarios
from app.routers import mascotas
from app.routers import tipos_perro
from app.routers import agendamientos
from app.routers import propietarios
from app.routers import tipos_servicio

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pet Shop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(mascotas.router)
app.include_router(tipos_perro.router)
app.include_router(agendamientos.router)
app.include_router(propietarios.router)
app.include_router(tipos_servicio.router)

@app.get("/")
def home():
    return {"mensaje": "API Pet Shop activa"}
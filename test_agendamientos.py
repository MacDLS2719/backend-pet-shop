import asyncio
from app.database import SessionLocal
from app import models
from app.schemas_pkg.agendamiento import AgendamientoResponse

def test():
    db = SessionLocal()
    agendamientos = db.query(models.Agendamiento).all()
    print(f"Found {len(agendamientos)} agendamientos")
    for a in agendamientos:
        try:
            AgendamientoResponse.model_validate(a)
            print("OK", a.id)
        except Exception as e:
            print("ERROR", a.id, e)

if __name__ == "__main__":
    test()

from sqlalchemy import text
from app.database import engine

def agregar_columna_politicas():
    with engine.connect() as connection:
        try:
            # Agrega la columna de aceptación de políticas de datos personales
            connection.execute(
                text("ALTER TABLE propietarios ADD COLUMN acepta_politicas BOOLEAN DEFAULT FALSE NOT NULL;")
            )
            connection.commit()
            print("✅ Columna 'acepta_politicas' agregada con éxito a la tabla 'propietarios'.")
        except Exception as e:
            print(f"⚠️ Nota / Error: {e}")

if __name__ == "__main__":
    agregar_columna_politicas()
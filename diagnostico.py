"""
Script de diagnostico: verifica el usuario en la DB y prueba bcrypt
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import bcrypt
from app.database import SessionLocal
from app.models import Usuario

def diagnosticar():
    db = SessionLocal()

    print("\n===== DIAGNOSTICO LOGIN =====\n")

    usuario = db.query(Usuario).filter(Usuario.username == "admin").first()

    if not usuario:
        print("USUARIO 'admin' NO encontrado en la DB")
        print("  -> Corre: python create_user.py")
        db.close()
        return

    print(f"Usuario encontrado : {usuario.username}")
    print(f"Email              : {usuario.email}")
    print(f"Activo             : {usuario.activo}")
    print(f"Hash (primeros 40) : {usuario.hashed_password[:40]}...")

    test_password = "123"

    try:
        resultado = bcrypt.checkpw(
            test_password.encode('utf-8'),
            usuario.hashed_password.encode('utf-8')
        )
        if resultado:
            print(f"\n[OK] bcrypt.checkpw('{test_password}') -> CORRECTO")
            print("     El login DEBE funcionar. Reinicia el backend con --reload")
        else:
            print(f"\n[FALLO] bcrypt.checkpw('{test_password}') -> INCORRECTO")
            print("     El hash no corresponde a '123'. Recrea el usuario.")
    except Exception as e:
        print(f"\n[ERROR] bcrypt fallo: {e}")

    db.close()
    print("\n=============================\n")

if __name__ == "__main__":
    diagnosticar()

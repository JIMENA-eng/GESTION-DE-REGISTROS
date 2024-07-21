# admin.py

from database import registrar_admin, buscar_admin

def registrar_administrador(username, password):
    registrar_admin(username, password)
    print(f"Administrador '{username}' registrado correctamente.")

def iniciar_sesion_administrador(username, password):
    admin = buscar_admin(username)
    if admin and admin[2] == password:  # admin[2] es la posición del campo 'password' en la tabla
        return True
    else:
        return False

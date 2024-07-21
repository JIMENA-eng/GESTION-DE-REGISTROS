# main.py

from tkinter import *
from tkinter import messagebox
from admin import registrar_administrador, iniciar_sesion_administrador
from api import consultar_api, registrar_persona
from database import inicializar_db, registrar_admin, buscar_admin, registrar_registro_dni, consultar_registro_dni

def abrir_ventana_registro_administrador():
    # Ocultar la ventana de inicio de sesión
    inicio_sesion_frame.pack_forget()

    # Mostrar la ventana de registro de administrador
    registro_admin_frame.pack(padx=20, pady=20)

def registrar_administrador():
    username = admin_username_registro_entry.get().strip()
    password = admin_password_registro_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Por favor complete todos los campos.")
        return

    registrar_admin(username, password)
    messagebox.showinfo("Éxito", f"Administrador '{username}' registrado correctamente.")
    registro_admin_frame.pack_forget()
    abrir_ventana_consulta_dni()

def iniciar_sesion_administrador():
    username = admin_username_entry.get().strip()
    password = admin_password_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Por favor complete todos los campos.")
        return

    if buscar_admin(username, password):
        # Ocultar la ventana de inicio de sesión
        inicio_sesion_frame.pack_forget()
        abrir_ventana_consulta_dni()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas.")

def abrir_ventana_consulta_dni():
    # Mostrar la ventana de consulta de DNI
    consulta_frame.pack(padx=20, pady=20)

def consultar_dni():
    dni = dni_entry.get().strip()

    if not dni:
        messagebox.showerror("Error", "Por favor ingrese un número de DNI.")
        return

    dni_registrado = consultar_registro_dni(dni)

    if dni_registrado:
        messagebox.showinfo("Éxito", f"El DNI {dni} está registrado en la base de datos.")
    else:
        messagebox.showwarning("Advertencia", f"El DNI {dni} no está registrado en la base de datos.")
        abrir_ventana_registro_dni()

def abrir_ventana_registro_dni():
    # Ocultar la ventana de consulta de DNI
    consulta_frame.pack_forget()

    # Mostrar la ventana de registro de DNI
    registro_frame.pack(padx=20, pady=20)

def registrar_dni():
    dni = dni_registro_entry.get().strip()

    if not dni:
        messagebox.showerror("Error", "Por favor ingrese un número de DNI.")
        return

    registrar_registro_dni(dni, 1)  # Se registra como 'registrado_en_api = 1'
    messagebox.showinfo("Éxito", f"DNI {dni} registrado en la base de datos correctamente.")
    registro_frame.pack_forget()
    abrir_ventana_consulta_dni()

# Inicializar la base de datos al inicio del programa
inicializar_db()

# Configuración de la interfaz gráfica
root = Tk()
root.title("Sistema de Registro de Asistencia - Administrador")

# Frame para inicio de sesión
inicio_sesion_frame = Frame(root)
inicio_sesion_frame.pack(padx=20, pady=20)

Label(inicio_sesion_frame, text="Inicio de Sesión de Administrador").grid(row=0, columnspan=2, padx=10, pady=5)

Label(inicio_sesion_frame, text="Username:").grid(row=1, column=0, padx=10, pady=5)
admin_username_entry = Entry(inicio_sesion_frame)
admin_username_entry.grid(row=1, column=1, padx=10, pady=5)

Label(inicio_sesion_frame, text="Password:").grid(row=2, column=0, padx=10, pady=5)
admin_password_entry = Entry(inicio_sesion_frame, show="*")
admin_password_entry.grid(row=2, column=1, padx=10, pady=5)

btn_registrar_admin = Button(inicio_sesion_frame, text="Registrar Administrador", command=abrir_ventana_registro_administrador)
btn_registrar_admin.grid(row=3, columnspan=2, padx=10, pady=10)

btn_iniciar_sesion = Button(inicio_sesion_frame, text="Iniciar Sesión", command=iniciar_sesion_administrador)
btn_iniciar_sesion.grid(row=4, columnspan=2, padx=10, pady=10)

# Frame para registro de administrador
registro_admin_frame = Frame(root, padx=20, pady=20)

Label(registro_admin_frame, text="Registro de Nuevo Administrador").grid(row=0, columnspan=2, padx=10, pady=5)

Label(registro_admin_frame, text="Username:").grid(row=1, column=0, padx=10, pady=5)
admin_username_registro_entry = Entry(registro_admin_frame)
admin_username_registro_entry.grid(row=1, column=1, padx=10, pady=5)

Label(registro_admin_frame, text="Password:").grid(row=2, column=0, padx=10, pady=5)
admin_password_registro_entry = Entry(registro_admin_frame, show="*")
admin_password_registro_entry.grid(row=2, column=1, padx=10, pady=5)

btn_registrar = Button(registro_admin_frame, text="Registrar", command=registrar_administrador)
btn_registrar.grid(row=3, columnspan=2, padx=10, pady=10)

# Frame para consulta de DNI
consulta_frame = Frame(root, padx=20, pady=20)

Label(consulta_frame, text="Consultar DNI").grid(row=0, columnspan=2, padx=10, pady=5)

Label(consulta_frame, text="Ingrese DNI:").grid(row=1, column=0, padx=10, pady=5)
dni_entry = Entry(consulta_frame)
dni_entry.grid(row=1, column=1, padx=10, pady=5)

btn_consultar_dni = Button(consulta_frame, text="Consultar", command=consultar_dni)
btn_consultar_dni.grid(row=2, columnspan=2, padx=10, pady=10)

# Frame para registro de DNI
registro_frame = Frame(root, padx=20, pady=20)

Label(registro_frame, text="Registrar DNI").grid(row=0, columnspan=2, padx=10, pady=5)

Label(registro_frame, text="Ingrese DNI:").grid(row=1, column=0, padx=10, pady=5)
dni_registro_entry = Entry(registro_frame)
dni_registro_entry.grid(row=1, column=1, padx=10, pady=5)

btn_registrar_dni = Button(registro_frame, text="Registrar", command=registrar_dni)
btn_registrar_dni.grid(row=2, columnspan=2, padx=10, pady=10)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()

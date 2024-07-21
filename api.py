import tkinter as tk
from tkinter import messagebox
import requests
import sqlite3
from datetime import datetime

# Función para consultar datos por API
def consultar_api(dni):
    url = f'https://api.reniec.cloud/dni/{dni}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la API: {str(e)}")
        return None

# Función para registrar una persona en la base de datos
def registrar_persona():
    nombre = nombre_entry.get()
    apellido_paterno = ap_paterno_entry.get()
    apellido_materno = ap_materno_entry.get()
    estado = estado_var.get()
    genero = genero_var.get()
    dni = dni_entry.get()
    fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Validación básica
    if not (nombre and apellido_paterno and dni):
        messagebox.showwarning("Datos incompletos", "Por favor complete todos los campos obligatorios (Nombre, Apellido Paterno, DNI).")
        return

    # Consultar datos del DNI en la API
    api_data = consultar_api(dni)
    if api_data:
        nombre_api = api_data.get('nombres', '')
        ap_paterno_api = api_data.get('apellido_paterno', '')
        ap_materno_api = api_data.get('apellido_materno', '')

        # Verificar que los datos coincidan
        if nombre.lower() != nombre_api.lower() or apellido_paterno.lower() != ap_paterno_api.lower() or apellido_materno.lower() != ap_materno_api.lower():
            messagebox.showwarning("Datos inconsistentes", "Los datos del DNI consultado no coinciden con los ingresados.")
            return

    try:
        conn = sqlite3.connect('registros.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS personas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT,
                            apellido_paterno TEXT,
                            apellido_materno TEXT,
                            estado TEXT,
                            genero TEXT,
                            dni TEXT,
                            fecha_hora TEXT)''')
        cursor.execute('''INSERT INTO personas (nombre, apellido_paterno, apellido_materno, estado, genero, dni, fecha_hora)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', (nombre, apellido_paterno, apellido_materno, estado, genero, dni, fecha_hora))
        conn.commit()
        conn.close()
        messagebox.showinfo("Registro exitoso", "Se registró la persona correctamente.")
    except sqlite3.Error as e:
        messagebox.showerror("Error de base de datos", f"No se pudo registrar la persona: {str(e)}")

# Función para mostrar registros de personas en una nueva ventana
def mostrar_registros():
    registros_window = tk.Toplevel(root)
    registros_window.title("Registros de Personas")
    registros_window.geometry("600x400")

    try:
        conn = sqlite3.connect('registros.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM personas')
        registros = cursor.fetchall()
        conn.close()

        if registros:
            tk.Label(registros_window, text="Registros de Personas:").pack()
            for registro in registros:
                tk.Label(registros_window, text=f"Nombre: {registro[1]} {registro[2]} {registro[3]}, Estado: {registro[4]}, Género: {registro[5]}, DNI: {registro[6]}, Fecha y hora: {registro[7]}").pack()
        else:
            tk.Label(registros_window, text="No hay registros disponibles.").pack()

    except sqlite3.Error as e:
        messagebox.showerror("Error de base de datos", f"No se pudo acceder a los registros: {str(e)}")

# Función para verificar las credenciales de administrador
def iniciar_sesion():
    usuario = usuario_entry.get()
    contrasena = contrasena_entry.get()

    # Verificación básica de usuario y contraseña (demostrativo)
    if usuario == "admin" and contrasena == "admin123":
        sesion_window.deiconify()  # Mostrar la ventana principal
        login_window.destroy()  # Cerrar la ventana de inicio de sesión
    else:
        messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos.")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Registro de Asistencia")
root.geometry("500x400")

# Ventana de inicio de sesión
login_window = tk.Toplevel(root)
login_window.title("Inicio de sesión")
login_window.geometry("300x150")

tk.Label(login_window, text="Usuario:").pack()
usuario_entry = tk.Entry(login_window)
usuario_entry.pack()

tk.Label(login_window, text="Contraseña:").pack()
contrasena_entry = tk.Entry(login_window, show="*")
contrasena_entry.pack()

tk.Button(login_window, text="Iniciar sesión", command=iniciar_sesion).pack()

# Ventana principal después de iniciar sesión
sesion_window = tk.Toplevel(root)
sesion_window.title("Registro de Asistencia - Sesión Administrador")
sesion_window.geometry("600x500")

tk.Label(sesion_window, text="Registro de Asistencia - Ingrese los datos:").pack()

tk.Label(sesion_window, text="Nombre:").pack()
nombre_entry = tk.Entry(sesion_window)
nombre_entry.pack()

tk.Label(sesion_window, text="Apellido Paterno:").pack()
ap_paterno_entry = tk.Entry(sesion_window)
ap_paterno_entry.pack()

tk.Label(sesion_window, text="Apellido Materno:").pack()
ap_materno_entry = tk.Entry(sesion_window)
ap_materno_entry.pack()

tk.Label(sesion_window, text="Estado:").pack()
estado_var = tk.StringVar(sesion_window)
estado_var.set("Asistió")
estado_options = ["Asistió", "No asistió", "Tardanza"]
estado_dropdown = tk.OptionMenu(sesion_window, estado_var, *estado_options)
estado_dropdown.pack()

tk.Label(sesion_window, text="Género:").pack()
genero_var = tk.StringVar(sesion_window)
genero_var.set("Masculino")
genero_options = ["Masculino", "Femenino"]
genero_dropdown = tk.OptionMenu(sesion_window, genero_var, *genero_options)
genero_dropdown.pack()

tk.Label(sesion_window, text="DNI:").pack()
dni_entry = tk.Entry(sesion_window)
dni_entry.pack()

tk.Button(sesion_window, text="Registrar Persona", command=registrar_persona).pack()
tk.Button(sesion_window, text="Consultar Registros", command=mostrar_registros).pack()

root.mainloop()

import tkinter as tk
from tkinter import messagebox
import requests

# Función para verificar el acceso como administrador
def verificar_acceso():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    
    # Validación básica (puedes cambiar esto según tu lógica de autenticación)
    if usuario == "admin" and contraseña == "12345":
        ventana_login.destroy()  # Cerrar la ventana de login
        mostrar_ventana_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Función para consultar el DNI en la API
def consultar_dni():
    dni = entry_dni.get()
    url = f'https://dniruc.apisperu.com/api/v1/dni/{dni}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkVjYXlvbWFAZ21haWwuY29tIn0.4w94GBUGg1bJmN50EiHBd1qHYEpnmjmS93lRP_7Nsr8'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            if 'dni' in response_json:
                mostrar_resultados(response_json)
            else:
                messagebox.showinfo("Información", f"DNI {dni} no encontrado en la API")
                mostrar_formulario_registro(dni)
        else:
            messagebox.showerror("Error", f"Error al consultar API: {response.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo conectar a la API: {str(e)}")

# Función para mostrar los resultados del DNI
def mostrar_resultados(datos_dni):
    ventana_resultados = tk.Toplevel()
    ventana_resultados.title("Resultados de Consulta")
    
    label_dni = tk.Label(ventana_resultados, text=f"DNI: {datos_dni['dni']}")
    label_dni.pack(padx=10, pady=5)
    
    label_nombres = tk.Label(ventana_resultados, text=f"Nombres: {datos_dni['nombres']}")
    label_nombres.pack(padx=10, pady=5)
    
    label_apellido_paterno = tk.Label(ventana_resultados, text=f"Apellido Paterno: {datos_dni['apellidoPaterno']}")
    label_apellido_paterno.pack(padx=10, pady=5)
    
    label_apellido_materno = tk.Label(ventana_resultados, text=f"Apellido Materno: {datos_dni['apellidoMaterno']}")
    label_apellido_materno.pack(padx=10, pady=5)

# Función para mostrar el formulario de registro si el DNI no está en la API
def mostrar_formulario_registro(dni):
    messagebox.showinfo("Información", f"Debe registrar el DNI {dni} en la base de datos")

# Configuración de la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Consulta de DNI")

frame_consulta = tk.Frame(ventana_principal)
frame_consulta.pack(padx=20, pady=20)

label_dni = tk.Label(frame_consulta, text="Ingrese DNI:")
label_dni.grid(row=0, column=0, padx=10, pady=5)
entry_dni = tk.Entry(frame_consulta)
entry_dni.grid(row=0, column=1, padx=10, pady=5)

btn_consultar = tk.Button(frame_consulta, text="Consultar", command=consultar_dni)
btn_consultar.grid(row=1, columnspan=2, padx=10, pady=10, sticky="ew")


# Función para mostrar la ventana principal después del login
def mostrar_ventana_principal():
    # Código para la ventana principal
    pass

# Función para mostrar los resultados del DNI
def mostrar_resultados(datos_dni):
    # Código para mostrar los resultados en la GUI
    pass

# Función para mostrar el formulario de registro si el DNI no está en la API
def mostrar_formulario_registro(dni):
    # Código para mostrar el formulario de registro en la GUI
    pass

# Configuración de la ventana de login
ventana_login = tk.Tk()
ventana_login.title("Login como Administrador")

frame_login = tk.Frame(ventana_login)
frame_login.pack(padx=20, pady=20)

label_usuario = tk.Label(frame_login, text="Usuario:")
label_usuario.grid(row=0, column=0, padx=10, pady=5)
entry_usuario = tk.Entry(frame_login)
entry_usuario.grid(row=0, column=1, padx=10, pady=5)

label_contraseña = tk.Label(frame_login, text="Contraseña:")
label_contraseña.grid(row=1, column=0, padx=10, pady=5)
entry_contraseña = tk.Entry(frame_login, show="*")
entry_contraseña.grid(row=1, column=1, padx=10, pady=5)

btn_login = tk.Button(frame_login, text="Iniciar Sesión", command=verificar_acceso)
btn_login.grid(row=2, columnspan=2, padx=10, pady=10, sticky="ew")

ventana_login.mainloop()

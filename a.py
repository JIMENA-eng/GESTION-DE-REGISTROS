import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import requests
import pandas as pd
from pandas import ExcelWriter

# Función para consultar con API (ejemplo con JSONPlaceholder)
def consultar_api():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
        data = response.json()
        messagebox.showinfo('Consulta API', f'Título del post: {data["title"]}')
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error', f'Error al consultar API: {str(e)}')

# Función para registrar manualmente
def registrar_manualmente():
    now = datetime.now()
    fecha_hora = now.strftime('%Y-%m-%d %H:%M:%S')
    messagebox.showinfo('Registro Manual', f'Registro realizado a las {fecha_hora}')

# Función para ver registros almacenados
def ver_registros():
    messagebox.showinfo('Registros', 'Aquí van los registros con fecha y hora de entrada y salida.')

# Función para exportar datos a PDF
def exportar_pdf():
    messagebox.showinfo('Exportar a PDF', 'Datos exportados a PDF.')

# Función para exportar datos a Excel
def exportar_excel():
    # Ejemplo básico de exportación a Excel usando pandas
    data = {'Nombre': ['Juan', 'María', 'Carlos'],
            'Edad': [25, 30, 35]}
    df = pd.DataFrame(data)
    writer = ExcelWriter('registros.xlsx')
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()
    messagebox.showinfo('Exportar a Excel', 'Datos exportados a Excel.')

# Función para iniciar sesión como administrador
def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    # Aquí se puede validar el usuario y contraseña
    if usuario == 'admin' and contrasena == 'admin123':
        messagebox.showinfo('Inicio de sesión', 'Sesión iniciada como administrador.')
        # Habilitar botones después del inicio de sesión
        btn_consultar_api.config(state=tk.NORMAL)
        btn_registrar_manualmente.config(state=tk.NORMAL)
        btn_ver_registros.config(state=tk.NORMAL)
        btn_exportar_pdf.config(state=tk.NORMAL)
        btn_exportar_excel.config(state=tk.NORMAL)
    else:
        messagebox.showerror('Error', 'Usuario o contraseña incorrectos.')

# Creación de la ventana principal
root = tk.Tk()
root.title('Sistema de Administrador')

# Etiquetas y entradas para usuario y contraseña
label_usuario = tk.Label(root, text='Usuario:')
label_usuario.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
entry_usuario = tk.Entry(root)
entry_usuario.grid(row=0, column=1, padx=10, pady=5)

label_contrasena = tk.Label(root, text='Contraseña:')
label_contrasena.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
entry_contrasena = tk.Entry(root, show='*')
entry_contrasena.grid(row=1, column=1, padx=10, pady=5)

# Botón para iniciar sesión
btn_iniciar_sesion = tk.Button(root, text='Iniciar sesión', command=iniciar_sesion)
btn_iniciar_sesion.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Botones para funciones disponibles después de iniciar sesión
btn_consultar_api = tk.Button(root, text='Consultar API', command=consultar_api, state=tk.DISABLED)
btn_consultar_api.grid(row=3, column=0, padx=10, pady=5)

btn_registrar_manualmente = tk.Button(root, text='Registrar manualmente', command=registrar_manualmente, state=tk.DISABLED)
btn_registrar_manualmente.grid(row=3, column=1, padx=10, pady=5)

btn_ver_registros = tk.Button(root, text='Ver registros', command=ver_registros, state=tk.DISABLED)
btn_ver_registros.grid(row=4, column=0, padx=10, pady=5)

btn_exportar_pdf = tk.Button(root, text='Exportar a PDF', command=exportar_pdf, state=tk.DISABLED)
btn_exportar_pdf.grid(row=4, column=1, padx=10, pady=5)

btn_exportar_excel = tk.Button(root, text='Exportar a Excel', command=exportar_excel, state=tk.DISABLED)
btn_exportar_excel.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Ejecutar el bucle principal
root.mainloop()

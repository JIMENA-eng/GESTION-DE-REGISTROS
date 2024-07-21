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
def iniciar_sesion_admin():
    top.destroy()  # Cerrar la ventana de selección de tipo de usuario
    admin_window = tk.Tk()
    admin_window.title('Inicio de sesión como Administrador')

    # Etiquetas y entradas para usuario y contraseña
    label_usuario = tk.Label(admin_window, text='Usuario:')
    label_usuario.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    entry_usuario = tk.Entry(admin_window)
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)

    label_contrasena = tk.Label(admin_window, text='Contraseña:')
    label_contrasena.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    entry_contrasena = tk.Entry(admin_window, show='*')
    entry_contrasena.grid(row=1, column=1, padx=10, pady=5)

    # Función para verificar el inicio de sesión como administrador
    def verificar_admin():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        # Validar usuario y contraseña
        if usuario == 'admin' and contrasena == 'admin123':
            admin_window.destroy()  # Cerrar la ventana de inicio de sesión
            # Abrir ventana principal del administrador
            ventana_administrador()
        else:
            messagebox.showerror('Error', 'Usuario o contraseña incorrectos.')

    # Botón para iniciar sesión como administrador
    btn_iniciar_sesion = tk.Button(admin_window, text='Iniciar sesión', command=verificar_admin)
    btn_iniciar_sesion.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    admin_window.mainloop()

# Función para la ventana principal del administrador
def ventana_administrador():
    admin_window = tk.Tk()
    admin_window.title('Panel de Administrador')

    # Botones para funciones disponibles
    btn_consultar_api = tk.Button(admin_window, text='Consultar API', command=consultar_api)
    btn_consultar_api.grid(row=0, column=0, padx=10, pady=5)

    btn_registrar_manualmente = tk.Button(admin_window, text='Registrar manualmente', command=registrar_manualmente)
    btn_registrar_manualmente.grid(row=0, column=1, padx=10, pady=5)

    btn_ver_registros = tk.Button(admin_window, text='Ver registros', command=ver_registros)
    btn_ver_registros.grid(row=1, column=0, padx=10, pady=5)

    btn_exportar_pdf = tk.Button(admin_window, text='Exportar a PDF', command=exportar_pdf)
    btn_exportar_pdf.grid(row=1, column=1, padx=10, pady=5)

    btn_exportar_excel = tk.Button(admin_window, text='Exportar a Excel', command=exportar_excel)
    btn_exportar_excel.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    admin_window.mainloop()

# Función para iniciar sesión como usuario
def iniciar_sesion_usuario():
    top.destroy()  # Cerrar la ventana de selección de tipo de usuario
    messagebox.showinfo('Inicio de sesión', 'Sesión iniciada como usuario.')
    # Aquí se pueden agregar las funciones para el usuario regular, si es necesario

# Crear la ventana principal para seleccionar tipo de usuario
top = tk.Tk()
top.title('Seleccionar tipo de usuario')

# Botones para seleccionar tipo de usuario
btn_admin = tk.Button(top, text='Iniciar sesión como Administrador', command=iniciar_sesion_admin)
btn_admin.pack(pady=20)

btn_usuario = tk.Button(top, text='Iniciar sesión como Usuario', command=iniciar_sesion_usuario)
btn_usuario.pack(pady=20)

top.mainloop()

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import requests
import pandas as pd
from pandas import ExcelWriter
from tkinter import filedialog

# Función para consultar datos del DNI
def consultar_dni():
    dni = entry_dni.get()
    if not dni:
        messagebox.showwarning('Advertencia', 'Por favor ingrese un número de DNI.')
        return

    try:
        # Aquí se simula una consulta a una API (puedes reemplazar esta URL con la que corresponda)
        # En este ejemplo, se asume que se obtiene información ficticia sobre el DNI ingresado
        url = f'https://dni.optimizeperu.com/api/persons/{dni}'
        response = requests.get(url)
        data = response.json()

        # Mostrar ventana con los datos del DNI
        mostrar_datos_dni(data)

    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error', f'Error al consultar datos del DNI: {str(e)}')

# Función para mostrar los datos del DNI en una nueva ventana
def mostrar_datos_dni(data):
    if data.get('success'):
        datos = data.get('data')

        # Crear y configurar ventana para mostrar datos del DNI
        ventana_datos = tk.Toplevel()
        ventana_datos.title('Datos del DNI')

        # Mostrar los datos obtenidos del DNI
        tk.Label(ventana_datos, text=f'Nombres: {datos["nombres"]}').pack()
        tk.Label(ventana_datos, text=f'Apellidos: {datos["apellidos"]}').pack()
        tk.Label(ventana_datos, text=f'Dirección: {datos["direccion"]}').pack()
        tk.Label(ventana_datos, text=f'Distrito: {datos["distrito"]}').pack()
        tk.Label(ventana_datos, text=f'Provincia: {datos["provincia"]}').pack()
        tk.Label(ventana_datos, text=f'Departamento: {datos["departamento"]}').pack()

        # Botón para cerrar la ventana
        tk.Button(ventana_datos, text='Cerrar', command=ventana_datos.destroy).pack()

    else:
        messagebox.showerror('Error', 'No se encontraron datos para el DNI proporcionado.')

# Función para iniciar sesión como administrador
def iniciar_sesion_admin():
    global top
    top = tk.Tk()
    top.title('Panel de Administrador')

    # Crear menú
    menu_bar = tk.Menu(top)

    # Menú de opciones
    opciones_menu = tk.Menu(menu_bar, tearoff=0)
    opciones_menu.add_command(label="Consultar API", command=consultar_dni)  # Función corregida
    opciones_menu.add_command(label="Registrar manualmente", command=registrar_manualmente)
    opciones_menu.add_separator()
    opciones_menu.add_command(label="Salir", command=top.quit)
    menu_bar.add_cascade(label="Opciones", menu=opciones_menu)

    # Menú de exportación
    exportar_menu = tk.Menu(menu_bar, tearoff=0)
    exportar_menu.add_command(label="Exportar a PDF", command=exportar_pdf)
    exportar_menu.add_command(label="Exportar a Excel", command=exportar_excel)
    menu_bar.add_cascade(label="Exportar", menu=exportar_menu)

    # Menú de registros
    registros_menu = tk.Menu(menu_bar, tearoff=0)
    registros_menu.add_command(label="Ver registros", command=ver_registros)
    menu_bar.add_cascade(label="Registros", menu=registros_menu)

    top.config(menu=menu_bar)

    # Etiqueta y entrada para ingresar el número de DNI
    tk.Label(top, text='Número de DNI:').pack(pady=10)
    global entry_dni
    entry_dni = tk.Entry(top)
    entry_dni.pack(pady=5)

    # Botón para consultar datos del DNI
    btn_consultar_dni = tk.Button(top, text='Consultar DNI', command=consultar_dni)
    btn_consultar_dni.pack(pady=10)

    top.mainloop()

# Función para iniciar sesión como usuario
def iniciar_sesion_usuario():
    global top
    top = tk.Tk()
    top.title('Panel de Usuario')
    messagebox.showinfo('Inicio de sesión', 'Sesión iniciada como usuario.')
    # Aquí se pueden agregar las funciones para el usuario regular, si es necesario

# Funciones de ejemplo para completar
def registrar_manualmente():
    pass

def exportar_pdf():
    pass

def exportar_excel():
    pass

def ver_registros():
    pass

# Crear la ventana principal para seleccionar tipo de usuario
top = tk.Tk()
top.title('Seleccionar tipo de usuario')

# Botones para seleccionar tipo de usuario
btn_admin = tk.Button(top, text='Iniciar sesión como Administrador', command=iniciar_sesion_admin)
btn_admin.pack(pady=20)

btn_usuario = tk.Button(top, text='Iniciar sesión como Usuario', command=iniciar_sesion_usuario)
btn_usuario.pack(pady=20)

top.mainloop()

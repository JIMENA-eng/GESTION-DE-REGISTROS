import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import requests
import pandas as pd
from pandas import ExcelWriter
from tkinter import filedialog

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

# Función para exportar datos a PDF
def exportar_pdf():
    try:
        # Ejemplo básico de exportación a PDF usando tkinter.filedialog
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            with open(filename, 'w') as f:
                f.write("Datos exportados a PDF.")
            messagebox.showinfo('Exportar a PDF', f'Datos exportados correctamente a:\n{filename}')
    except Exception as e:
        messagebox.showerror('Error', f'Error al exportar a PDF: {str(e)}')

# Función para exportar datos a Excel
def exportar_excel():
    try:
        # Ejemplo básico de exportación a Excel usando pandas y tkinter.filedialog
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if filename:
            data = {'Nombre': ['Juan', 'María', 'Carlos'],
                    'Edad': [25, 30, 35]}
            df = pd.DataFrame(data)
            writer = ExcelWriter(filename)
            df.to_excel(writer, 'Sheet1', index=False)
            writer.save()
            messagebox.showinfo('Exportar a Excel', f'Datos exportados correctamente a:\n{filename}')
    except Exception as e:
        messagebox.showerror('Error', f'Error al exportar a Excel: {str(e)}')

# Función para ver registros almacenados
def ver_registros():
    messagebox.showinfo('Registros', 'Aquí van los registros con fecha y hora de entrada y salida.')

# Función para iniciar sesión como administrador
def iniciar_sesion_admin():
    top.destroy()  # Cerrar la ventana de selección de tipo de usuario
    admin_window = tk.Tk()
    admin_window.title('Panel de Administrador')

    # Crear menú
    menu_bar = tk.Menu(admin_window)

    # Menú de opciones
    opciones_menu = tk.Menu(menu_bar, tearoff=0)
    opciones_menu.add_command(label="Consultar API", command=consultar_api)
    opciones_menu.add_command(label="Registrar manualmente", command=registrar_manualmente)
    opciones_menu.add_separator()
    opciones_menu.add_command(label="Salir", command=admin_window.quit)
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

    admin_window.config(menu=menu_bar)

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


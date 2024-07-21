import tkinter as tk
from tkinter import messagebox
import requests

# Función para consultar datos del DNI usando la primera API
def consultar_dni_api1():
    dni = entry_dni.get()
    if not dni:
        messagebox.showwarning('Advertencia', 'Por favor ingrese un número de DNI.')
        return

    try:
        url = f'https://dni.optimizeperu.com/api/persons/{dni}'
        response = requests.get(url)
        data = response.json()

        if 'nombres' in data:
            mostrar_datos_dni(data)
        else:
            messagebox.showerror('Error', 'No se encontraron datos para el DNI proporcionado.')

    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error', f'Error al consultar datos del DNI: {str(e)}')

    except ValueError as ve:
        messagebox.showerror('Error', f'Error al parsear respuesta JSON: {str(ve)}')

# Función para consultar datos del DNI usando la segunda API
def consultar_dni_api2():
    dni = entry_dni.get()
    if not dni:
        messagebox.showwarning('Advertencia', 'Por favor ingrese un número de DNI.')
        return

    try:
        url = f'https://dniruc.apisperu.com/api/v1/dni/{dni}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkVjYXlvbWFAZ21haWwuY29tIn0.4w94GBUGg1bJmN50EiHBd1qHYEpnmjmS93lRP_7Nsr8'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            if 'success' in data and data['success'] == True:
                mostrar_datos_dni(data)
            else:
                messagebox.showerror('Error', 'No se encontraron datos para el DNI proporcionado.')
        else:
            messagebox.showerror('Error', 'Error en la consulta a la API.')

    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error', f'Error al consultar datos del DNI: {str(e)}')

    except ValueError as ve:
        messagebox.showerror('Error', f'Error al parsear respuesta JSON: {str(ve)}')

# Función para mostrar los datos del DNI en una nueva ventana
def mostrar_datos_dni(data):
    try:
        ventana_datos = tk.Toplevel()
        ventana_datos.title('Datos del DNI')

        if data.get('success'):
            datos = data.get('data')

            tk.Label(ventana_datos, text=f'Nombres: {datos.get("nombres", "No disponible")}').pack()
            tk.Label(ventana_datos, text=f'Apellidos: {datos.get("apellidoPaterno", "No disponible")} {datos.get("apellidoMaterno", "No disponible")}').pack()
            tk.Label(ventana_datos, text=f'Dirección: {datos.get("direccion", "No disponible")}').pack()
            tk.Label(ventana_datos, text=f'Distrito: {datos.get("distrito", "No disponible")}').pack()
            tk.Label(ventana_datos, text=f'Provincia: {datos.get("provincia", "No disponible")}').pack()
            tk.Label(ventana_datos, text=f'Departamento: {datos.get("departamento", "No disponible")}').pack()

        else:
            messagebox.showerror('Error', 'No se encontraron datos para el DNI proporcionado.')

        btn_cerrar = tk.Button(ventana_datos, text='Cerrar', command=ventana_datos.destroy)
        btn_cerrar.pack()

    except Exception as e:
        messagebox.showerror('Error', f'Error al mostrar datos del DNI: {str(e)}')

# Función para iniciar sesión como administrador
def iniciar_sesion_admin():
    global top
    top = tk.Tk()
    top.title('Panel de Administrador')

    menu_bar = tk.Menu(top)

    opciones_menu = tk.Menu(menu_bar, tearoff=0)
    opciones_menu.add_command(label="Consultar DNI (API 1)", command=consultar_dni_api1)
    opciones_menu.add_command(label="Consultar DNI (API 2)", command=consultar_dni_api2)
    opciones_menu.add_command(label="Registrar manualmente", command=registrar_manualmente)
    opciones_menu.add_separator()
    opciones_menu.add_command(label="Salir", command=top.quit)
    menu_bar.add_cascade(label="Opciones", menu=opciones_menu)

    exportar_menu = tk.Menu(menu_bar, tearoff=0)
    exportar_menu.add_command(label="Exportar a PDF", command=exportar_pdf)
    exportar_menu.add_command(label="Exportar a Excel", command=exportar_excel)
    menu_bar.add_cascade(label="Exportar", menu=exportar_menu)

    registros_menu = tk.Menu(menu_bar, tearoff=0)
    registros_menu.add_command(label="Ver registros", command=ver_registros)
    menu_bar.add_cascade(label="Registros", menu=registros_menu)

    top.config(menu=menu_bar)

    tk.Label(top, text='Número de DNI:').pack(pady=10)
    global entry_dni
    entry_dni = tk.Entry(top)
    entry_dni.pack(pady=5)

    btn_consultar_dni = tk.Button(top, text='Consultar DNI (API 2)', command=consultar_dni_api2)
    btn_consultar_dni.pack(pady=10)

    top.mainloop()

# Función para iniciar sesión como usuario
def iniciar_sesion_usuario():
    global top
    top = tk.Tk()
    top.title('Panel de Usuario')
    messagebox.showinfo('Inicio de sesión', 'Sesión iniciada como usuario.')

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

btn_admin = tk.Button(top, text='Iniciar sesión como Administrador', command=iniciar_sesion_admin)
btn_admin.pack(pady=20)

btn_usuario = tk.Button(top, text='Iniciar sesión como Usuario', command=iniciar_sesion_usuario)
btn_usuario.pack(pady=20)

top.mainloop()

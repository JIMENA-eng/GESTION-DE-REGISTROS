import tkinter as tk
from tkinter import messagebox, ttk
import requests
import sqlite3

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Consulta de DNI y Asistencia")
        
        self.frame_login = tk.Frame(self.root)
        self.frame_login.pack(pady=20)
        
        self.label_username = tk.Label(self.frame_login, text="Usuario:")
        self.label_username.grid(row=0, column=0, padx=10, pady=10)
        self.entry_username = tk.Entry(self.frame_login)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)
        
        self.label_password = tk.Label(self.frame_login, text="Contraseña:")
        self.label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password = tk.Entry(self.frame_login, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)
        
        self.button_login = tk.Button(self.frame_login, text="Iniciar sesión", command=self.login)
        self.button_login.grid(row=2, columnspan=2, padx=10, pady=10)
        
        # Conexión y creación de la base de datos SQLite
        self.conn = sqlite3.connect('RE')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS registros (
                            dni TEXT PRIMARY KEY,
                            nombres TEXT,
                            apellido_paterno TEXT,
                            apellido_materno TEXT,
                            genero TEXT,
                            estado_civil TEXT,
                            asistencia INTEGER
                            )''')
        self.conn.commit()
        
    def login(self):
        # Aquí podrías implementar la lógica de autenticación de administrador
        # Por simplicidad, vamos a suponer que cualquier usuario y contraseña son válidos
        # Esto es solo un ejemplo, no es seguro en un entorno real.
        # Idealmente, deberías tener un sistema seguro de autenticación.
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if username == "admin" and password == "password":
            self.show_dni_entry()
        else:
            messagebox.showerror("Error de autenticación", "Credenciales incorrectas")
        
    def show_dni_entry(self):
        self.frame_login.destroy()
        
        self.frame_dni = tk.Frame(self.root)
        self.frame_dni.pack(pady=20)
        
        self.label_dni = tk.Label(self.frame_dni, text="Ingrese el DNI:")
        self.label_dni.grid(row=0, column=0, padx=10, pady=10)
        self.entry_dni = tk.Entry(self.frame_dni)
        self.entry_dni.grid(row=0, column=1, padx=10, pady=10)
        
        self.button_consultar = tk.Button(self.frame_dni, text="Consultar", command=self.consultar_dni)
        self.button_consultar.grid(row=1, columnspan=2, padx=10, pady=10)
        
    def consultar_dni(self):
        dni = self.entry_dni.get()
        url = f'https://dniruc.apisperu.com/api/v1/dni/{dni}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkVjYXlvbWFAZ21haWwuY29tIn0.4w94GBUGg1bJmN50EiHBd1qHYEpnmjmS93lRP_7Nsr8'
        
        response = requests.get(url)
        
        if response.status_code == 200:
            response_json = response.json()
            if not response_json['success']:
                messagebox.showinfo("DNI no registrado", "El DNI no se encuentra registrado.")
                self.registrar_dni()
            else:
                self.mostrar_datos(response_json)
        else:
            messagebox.showerror("Error en la consulta", f"Código de estado: {response.status_code}")
    
    def mostrar_datos(self, response_json):
        messagebox.showinfo("Datos personales",
                            f"DNI: {response_json['dni']}\n"
                            f"Nombres: {response_json['nombres']}\n"
                            f"Apellido Paterno: {response_json['apellidoPaterno']}\n"
                            f"Apellido Materno: {response_json['apellidoMaterno']}")
        
        # Verificar si el DNI ya está registrado antes de registrar la asistencia
        dni = response_json['dni']
        self.c.execute("SELECT * FROM registros WHERE dni=?", (dni,))
        existing_record = self.c.fetchone()
        
        if existing_record:
            self.registrar_asistencia(response_json)
        else:
            messagebox.showinfo("Registro necesario", "El DNI necesita ser registrado.")
            self.registrar_dni()
    
    def registrar_dni(self):
        self.frame_dni.destroy()
        
        self.frame_registro = tk.Frame(self.root)
        self.frame_registro.pack(pady=20)
        
        self.label_registro = tk.Label(self.frame_registro, text="Registro de datos:")
        self.label_registro.grid(row=0, column=0, padx=10, pady=10)
        
        self.label_dni_registro = tk.Label(self.frame_registro, text="DNI:")
        self.label_dni_registro.grid(row=1, column=0, padx=10, pady=10)
        self.entry_dni_registro = tk.Entry(self.frame_registro)
        self.entry_dni_registro.grid(row=1, column=1, padx=10, pady=10)
        
        self.label_nombres = tk.Label(self.frame_registro, text="Nombres:")
        self.label_nombres.grid(row=2, column=0, padx=10, pady=10)
        self.entry_nombres = tk.Entry(self.frame_registro)
        self.entry_nombres.grid(row=2, column=1, padx=10, pady=10)
        
        self.label_apellido_paterno = tk.Label(self.frame_registro, text="Apellido Paterno:")
        self.label_apellido_paterno.grid(row=3, column=0, padx=10, pady=10)
        self.entry_apellido_paterno = tk.Entry(self.frame_registro)
        self.entry_apellido_paterno.grid(row=3, column=1, padx=10, pady=10)
        
        self.label_apellido_materno = tk.Label(self.frame_registro, text="Apellido Materno:")
        self.label_apellido_materno.grid(row=4, column=0, padx=10, pady=10)
        self.entry_apellido_materno = tk.Entry(self.frame_registro)
        self.entry_apellido_materno.grid(row=4, column=1, padx=10, pady=10)
        
        self.button_guardar_registro = tk.Button(self.frame_registro, text="Guardar registro", command=self.guardar_registro)
        self.button_guardar_registro.grid(row=5, columnspan=2, padx=10, pady=10)
    
    def guardar_registro(self):
        dni = self.entry_dni_registro.get()
        nombres = self.entry_nombres.get()
        apellido_paterno = self.entry_apellido_paterno.get()
        apellido_materno = self.entry_apellido_materno.get()
        
        try:
            # Intentar insertar el registro
            self.c.execute('''INSERT INTO registros (dni, nombres, apellido_paterno, apellido_materno, genero, estado_civil, asistencia)
                              VALUES (?, ?, ?, ?, NULL, NULL, 0)''',
                           (dni, nombres, apellido_paterno, apellido_materno))
            self.conn.commit()
            
            messagebox.showinfo("Registro guardado", f"Se ha guardado el registro de {nombres} {apellido_paterno} {apellido_materno}.")
            self.show_dni_entry()
        
        except sqlite3.IntegrityError:
            # Si hay un error de integridad (clave primaria duplicada)
            messagebox.showerror("Error", f"El DNI {dni} ya está registrado en la base de datos.")

    def registrar_asistencia(self, response_json):
        self.frame_dni.destroy()
        
        self.frame_asistencia = tk.Frame(self.root)
        self.frame_asistencia.pack(pady=20)
        
        self.label_dni = tk.Label(self.frame_asistencia, text=f"DNI: {response_json['dni']}")
        self.label_dni.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        self.label_genero = tk.Label(self.frame_asistencia, text="Género:")
        self.label_genero.grid(row=1, column=0, padx=10, pady=10)
        self.entry_genero = tk.Entry(self.frame_asistencia)
        self.entry_genero.grid(row=1, column=1, padx=10, pady=10)
        
        self.label_estado_civil = tk.Label(self.frame_asistencia, text="Estado Civil:")
        self.label_estado_civil.grid(row=2, column=0, padx=10, pady=10)
        self.entry_estado_civil = tk.Entry(self.frame_asistencia)
        self.entry_estado_civil.grid(row=2, column=1, padx=10, pady=10)
        
        self.button_genero_m = tk.Button(self.frame_asistencia, text="Masculino", command=lambda: self.seleccionar_genero("Masculino"))
        self.button_genero_m.grid(row=3, column=0, padx=10, pady=10)
        
        self.button_genero_f = tk.Button(self.frame_asistencia, text="Femenino", command=lambda: self.seleccionar_genero("Femenino"))
        self.button_genero_f.grid(row=3, column=1, padx=10, pady=10)
        
        self.button_estado_soltero = tk.Button(self.frame_asistencia, text="Soltero", command=lambda: self.seleccionar_estado("Soltero"))
        self.button_estado_soltero.grid(row=4, column=0, padx=10, pady=10)
        
        self.button_estado_casado = tk.Button(self.frame_asistencia, text="Casado", command=lambda: self.seleccionar_estado("Casado"))
        self.button_estado_casado.grid(row=4, column=1, padx=10, pady=10)
        
        self.button_registrar_asistencia = tk.Button(self.frame_asistencia, text="Registrar Asistencia", command=lambda: self.guardar_asistencia(response_json))
        self.button_registrar_asistencia.grid(row=5, columnspan=2, padx=10, pady=10)
    
    def seleccionar_genero(self, genero):
        self.entry_genero.delete(0, tk.END)
        self.entry_genero.insert(0, genero)
    
    def seleccionar_estado(self, estado):
        self.entry_estado_civil.delete(0, tk.END)
        self.entry_estado_civil.insert(0, estado)
    
    def guardar_asistencia(self, response_json):
        dni = response_json['dni']
        genero = self.entry_genero.get()
        estado_civil = self.entry_estado_civil.get()
        
        try:
            # Intentar actualizar el registro de asistencia
            self.c.execute('''UPDATE registros 
                              SET genero=?, estado_civil=?, asistencia=1
                              WHERE dni=?''',
                           (genero, estado_civil, dni))
            self.conn.commit()
            
            messagebox.showinfo("Asistencia registrada", f"Se ha registrado la asistencia de {dni}.")
            self.mostrar_datos(response_json)  # Mostrar ventana con datos completos
        
        except sqlite3.IntegrityError:
            # Si hay un error de integridad (clave primaria duplicada)
            messagebox.showerror("Error", f"El DNI {dni} ya está registrado en la base de datos.")
    
    def mostrar_ventana_datos(self, response_json):
        ventana_datos = tk.Toplevel(self.root)
        ventana_datos.title("Datos Completos")
        
        tk.Label(ventana_datos, text=f"DNI: {response_json['dni']}").pack(padx=10, pady=5)
        tk.Label(ventana_datos, text=f"Nombres: {response_json['nombres']}").pack(padx=10, pady=5)
        tk.Label(ventana_datos, text=f"Apellido Paterno: {response_json['apellidoPaterno']}").pack(padx=10, pady=5)
        tk.Label(ventana_datos, text=f"Apellido Materno: {response_json['apellidoMaterno']}").pack(padx=10, pady=5)
        tk.Label(ventana_datos, text=f"Género: {self.entry_genero.get()}").pack(padx=10, pady=5)
        tk.Label(ventana_datos, text=f"Estado Civil: {self.entry_estado_civil.get()}").pack(padx=10, pady=5)
        
        tk.Button(ventana_datos, text="Cerrar", command=ventana_datos.destroy).pack(padx=10, pady=10)
    
    def __del__(self):
        self.conn.close()

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

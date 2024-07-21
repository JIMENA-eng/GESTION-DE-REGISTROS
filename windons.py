from tkinter import*
from tkinter import ttk,messagebox
from avisos import*
from estructura import*
import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



# Función para iniciar sesión como administrador
def iniciar_sesion_admin():
    top.destroy()  # Cerrar la ventana de selección de tipo de usuario
    root=Tk()
    root.title('Inicio de sesión como Administrador')

    # Etiquetas y entradas para usuario y contraseña
    label_usuario = tk.Label(root, text='Usuario:')
    label_usuario.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    entry_usuario = tk.Entry(root)
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)

    label_contrasena = tk.Label(root, text='Contraseña:')
    label_contrasena.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    entry_contrasena = tk.Entry(root, show='*')
    entry_contrasena.grid(row=1, column=1, padx=10, pady=5)

    # Función para verificar el inicio de sesión como administrador
    def verificar_admin():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        # Validar usuario y contraseña
        if usuario == 'admin' and contrasena == 'admin123':
            root.destroy()  # Cerrar la ventana de inicio de sesión
            # Abrir ventana principal del administrador
            ventana_administrador()
        else:
            messagebox.showerror('Error', 'Usuario o contraseña incorrectos.')

    # Botón para iniciar sesión como administrador
    btn_iniciar_sesion = tk.Button(root, text='Iniciar sesión', command=verificar_admin)
    btn_iniciar_sesion.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

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

def DNI():

    # Función para consultar el DNI en la API
    def dni_consultar():
        dni = entry_dni.get()
        if not dni:
            messagebox.showwarning('Advertencia', 'Por favor ingrese un número de DNI.')
            return

        try:
            # URL de la API para consultar el DNI
            url = f'https://dniruc.apisperu.com/api/v1/dni/{dni}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkVjYXlvbWFAZ21haWwuY29tIn0.4w94GBUGg1bJmN50EiHBd1qHYEpnmjmS93lRP_7Nsr8'
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción si ocurre un error en la solicitud

            data = response.json()

            if response.status_code == 200:
                if not data['success']:
                    messagebox.showinfo("DNI no registrado", "El DNI no se encuentra registrado.")
                else:
                    mostrar_datos(data)
            else:
                messagebox.showerror("Error en la consulta", f"Código de estado: {response.status_code}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error en la consulta", f"Error de conexión: {str(e)}")

    # Función para mostrar los datos del DNI en una ventana y guardarlos en la base de datos
    def mostrar_datos(data):
        wen.destroy()
        ventana_datos = tk.Toplevel()
        ventana_datos.title('Datos del DNI')

        tk.Label(ventana_datos, text=f'DNI: {data["dni"]}').pack(padx=10, pady=5)
        tk.Label(ventana_datos, text=f'Nombres: {data["nombres"]}').pack(padx=10, pady=5)
        tk.Label(ventana_datos, text=f'Apellido Paterno: {data["apellidoPaterno"]}').pack(padx=10, pady=5)
        tk.Label(ventana_datos, text=f'Apellido Materno: {data["apellidoMaterno"]}').pack(padx=10, pady=5)

        # Sección para ingresar el estado civil
        frame_estado_civil = tk.LabelFrame(ventana_datos, text="Estado Civil")
        frame_estado_civil.pack(padx=10, pady=5, fill="both", expand="yes")

        estado_civil_options = ["Soltero/a", "Casado/a", "Viudo/a", "Divorciado/a", "Conviviente", "Otro"]

        estado_civil = tk.StringVar()
        estado_civil.set("")  # Valor inicial

        for option in estado_civil_options:
            tk.Radiobutton(frame_estado_civil, text=option, variable=estado_civil, value=option).pack(anchor="w")

        # Botones de género (ejemplo básico)
        tk.Label(ventana_datos, text="Género:").pack(padx=10, pady=5)
        tk.Button(ventana_datos, text="Femenino", command=lambda: guardar_en_db(data, "Femenino", estado_civil.get())).pack(pady=5)
        tk.Button(ventana_datos, text="Masculino", command=lambda: guardar_en_db(data, "Masculino", estado_civil.get())).pack(pady=5)
        tk.Button(ventana_datos, text="Otros", command=lambda: guardar_en_db(data, "Otros", estado_civil.get())).pack(pady=5)

        # Botón para cerrar ventana
        btn_cerrar = tk.Button(ventana_datos, text='registrar', command=ventana_datos.destroy)
        btn_cerrar.pack(pady=10)

    def guardar_en_db(data, genero, estado_civil):
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('registro_asistencia')
            cursor = conn.cursor()

            # Obtener la fecha y hora actual
            fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insertar los datos en la tabla 'asistencia' junto con la fecha y hora
            cursor.execute('''
                INSERT INTO asistencia (NOMBRES, APELLIDO_PATERNO, APELLIDO_MATERNO, DNI, GENERO, ESTADO_CIVIL, FECHA_HORA)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data["nombres"], data["apellidoPaterno"], data["apellidoMaterno"], data["dni"], genero, estado_civil, fecha_hora_actual))

            # Guardar cambios y cerrar la conexión
            conn.commit()
            conn.close()

            messagebox.showinfo("Registro exitoso", "Los datos se han guardado correctamente en la base de datos.")

        except sqlite3.Error as e:
            messagebox.showerror("Error al guardar", f"Error de SQLite: {str(e)}")

    # Crear la ventana principal
    wen = tk.Tk()
    wen.title('Consulta de DNI')

    # Etiqueta y entrada para ingresar el número de DNI
    label_dni = tk.Label(wen, text='Ingrese el número de DNI:')
    label_dni.pack(pady=10)

    entry_dni = tk.Entry(wen)
    entry_dni.pack(pady=5)

    # Botón para consultar el DNI (se activará también con Enter)
    btn_consultar = tk.Button(wen, text='Consultar DNI', command=dni_consultar)
    btn_consultar.pack(pady=10)

    # Atajo para activar la función dni_consultar al presionar Enter en la entrada de texto
    entry_dni.bind('<Return>', lambda event: dni_consultar())

    wen.mainloop()

def PDF():

    def exportar_a_pdf():
        # Conectar a la base de datos SQLite
        conn = sqlite3.connect('registro_asistencia')
        cursor = conn.cursor()

        # Obtener los datos de la tabla asistencia
        cursor.execute('SELECT * FROM asistencia')
        datos = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        conn.close()

        # Crear el archivo PDF
        pdf_filename = 'exportacion_asistencia.pdf'
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        
        # Configurar el tamaño y la posición de la tabla en el PDF
        width, height = letter
        table_width = width - 80
        table_height = height - 80
        col_widths = [50, 120, 120, 80, 80, 80, 100]
        y_start = table_height - 50

        # Configurar encabezados de columna
        encabezados = ['ID', 'Nombres', 'Apellido Paterno', 'Apellido Materno', 'DNI', 'Género', 'Estado Civil']
        
        # Dibujar encabezados de columna
        for i, encabezado in enumerate(encabezados):
            c.drawString(40 + sum(col_widths[:i]), y_start, encabezado)
        
        y_start -= 20
        
        # Dibujar los datos de la tabla
        for dato in datos:
            for i, valor in enumerate(dato):
                c.drawString(40 + sum(col_widths[:i]), y_start, str(valor))
            y_start -= 15
        
        # Guardar el PDF y finalizar
        c.save()
        print(f'Se ha exportado exitosamente la base de datos a {pdf_filename}')

    # Ejecutar la función para exportar a PDF
    exportar_a_pdf()

def EXCEL():
    def exportar_a_excel():
    # Conectar a la base de datos SQLite
        conn = sqlite3.connect('tu_base_de_datos.db')

        # Consultar datos desde SQLite utilizando pandas
        query = "SELECT * FROM asistencia"
        df = pd.read_sql_query(query, conn)

        # Cerrar la conexión a la base de datos
        conn.close()

        # Especificar el nombre del archivo Excel
        excel_filename = 'exportacion_asistencia.xlsx'

        # Exportar DataFrame a Excel
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Asistencia', index=False)

        print(f'Se ha exportado exitosamente la base de datos a {excel_filename}')

    # Ejecutar la función para exportar a Excel
    exportar_a_excel()
    
miid=StringVar()
minombres=StringVar()
miapellido_paterno=StringVar()
miapellido_materno=StringVar()
midni=StringVar()
migenero=StringVar()
miestado_civil=StringVar()

def ventana_administrador():
    
    def conexion():
        Estructura.conexion()

    def eliminar():
        Estructura.eliminar()
        limpiarmostrar()
        
    def consultar_dni():
        Estructura.consultar_dni()

    def limpiarmostrar():
        limpiarcampos()
        mostrar()
        
    def limpiarcampos():
        miid.set("")
        minombres.set("")
        miapellido_paterno.set("")
        miapellido_materno.set("")
        midni.set("")
        migenero.set("")
        miestado_civil.set("")
        
    def mostrar():
        Estructura.mostrar(tree)
        
    def salirAplicacion():
        valor=messagebox.askquestion("salir",Avisos.SALIR)
        root.destroy() if valor == "yes" else None


    def crear():
        Estructura.crear(minombres.get(),miapellido_paterno.get(),miapellido_materno.get(),midni.get(),migenero.get(),miestado_civil.get())
        limpiarmostrar()
        
    def actualizar():
        Estructura.actualizar(minombres.get(),miapellido_paterno.get(),miapellido_materno.get(),midni.get(),migenero.get(),miestado_civil.get(), miid.get())
        limpiarmostrar()

    def borrar():
        Estructura.borrar(miid.get())
        limpiarmostrar()

    def seleccionarUsandioClick(event):
        item=tree.identify('item',event.x,event.y)
        miid.set(tree.item(item,"text"))
        minombres.set(tree.item(item,"values")[0])
        miapellido_paterno.set(tree.item(item,"values")[1])
        miapellido_materno.set(tree.item(item,"values")[2])
        midni.set(tree.item(item,"values")[3])
        migenero.set(tree.item(item,"values")[4])
        miestado_civil.set(tree.item(item,"values")[5])
    


    root=Tk()
    root.title("REGISTRO Y ASISTENCIA")
    root.configure(background='lightpink')
    root.geometry("800x900")
    
    menubar=Menu(root)
    menubasedat=Menu(menubar,tearoff=0)
    menubasedat.add_command(label="crear/conectar base de datos", command=conexion)
    menubasedat.add_command(label="eliminar la base de datos", command=eliminar)
    menubasedat.add_command(label="salir", command=salirAplicacion)
    menubar.add_cascade(label="inicio",menu=menubasedat)

    consultarmenu=Menu(menubar, tearoff=0)
    consultarmenu.add_command(label="DNI", command=DNI)
    menubar.add_cascade(label="consultar", menu=consultarmenu)

    repormenu=Menu(menubar, tearoff=0)
    repormenu.add_command(label="reporte diario")
    repormenu.add_command(label="reporte semanal")
    repormenu.add_command(label="reporte mensual")
    menubar.add_cascade(label="reportes", menu=repormenu)

    expomenu=Menu(menubar, tearoff=0)
    expomenu.add_command(label="exportar datos a excel", command=EXCEL)
    expomenu.add_command(label="descargar datos en pdf",command=PDF)
    menubar.add_cascade(label="exportar", menu=expomenu)
    
    lectormenu=Menu(menubar, tearoff=0)
    lectormenu.add_command(label="lector digiatal de dni")
    menubar.add_cascade(label="escaneo", menu=lectormenu)
    
    

    ayudamenu=Menu(menubar,tearoff=0)
    ayudamenu.add_command(label="resetear campos", command=limpiarcampos)
    ayudamenu.add_command(label="acerca", command=Estructura.mensaje)
    menubar.add_cascade(label="ayuda", menu=ayudamenu)
    
    cabecera1=["id","nombre","apellido paterno","apellido materno","dni"]
    tree=ttk.Treeview(height=10, columns=('#0', '#1','#2','#3','#4'))
    tree.place(x=0, y=200)
    tree.column('#0', width=150)
    tree.heading('#0', text=cabecera1[0], anchor=CENTER)
    tree.heading('#1', text=cabecera1[1], anchor=CENTER)
    tree.heading('#2', text=cabecera1[2], anchor=CENTER)
    tree.heading('#3', text=cabecera1[3], anchor=CENTER)
    tree.heading('#4', text=cabecera1[4], anchor=CENTER)

    cabecera2=["id", "dni","genero","estado civil","fecha y hora"]
    tree=ttk.Treeview(height=10, columns=('#0','#1','#2','#3','#4'))
    tree.place(x=0,y=400)
    tree.column('#0', width=150)
    tree.heading('#0', text=cabecera2[0], anchor=CENTER)
    tree.heading('#1', text=cabecera2[1], anchor=CENTER)
    tree.heading('#2', text=cabecera2[2], anchor=CENTER)
    tree.heading('#3', text=cabecera2[3], anchor=CENTER)
    tree.heading('#4', text=cabecera2[4], anchor=CENTER)
    tree.bind("<Button-1>", seleccionarUsandioClick)
    mostrar()
        

    e1=Entry(root, textvariable=miid)

    l2=Label(root, text="DNI").place(x=50,y=10)
    e2=Entry(root, textvariable=midni, width=50).place(x=100,y=10)

    l3=Label(root, text="NOMBRES").place(x=50, y=40)
    e3=Entry(root, textvariable=minombres).place(x=130, y=40)

    l4=Label(root, text="APELLIDO PATERNO").place(x=50, y=70)
    e4=Entry(root, textvariable=miapellido_paterno).place(x=180, y=70)

    l5=Label(root, text="APELLIDO MATERNO").place(x=50, y=100)
    e5=Entry(root, textvariable=miapellido_materno).place(x=180, y=100)

    l6=Label(root, text="GENERO").place(x=50, y=130)
    e6=Entry(root, textvariable=migenero).place(x=100, y=130)

    l7=Label(root, text="ESTADO CIVIL").place(x=280, y=130)
    e7=Entry(root, textvariable=miestado_civil, width=10).place(x=380,y=130)
    
    
    
    b0=Button(root, text="buscar registro", command=consultar_dni).place(x=550, y=10)
    b1=Button(root, text="crear registro", command=crear).place(x=70, y=160)
    b2=Button(root, text="actualizar registro", command=actualizar).place(x=230, y=160)
    b3=Button(root, text="mostrar registro", command=mostrar).place(x=550,y=160)
    b4=Button(root, text="eliminar registro", bg="red", command=borrar).place(x=950, y=160)
    
    
                
    root.config(menu=menubar)



if __name__ == "__main__":
    root = tk.Tk()
    top.mainloop()
    root.mainloop()


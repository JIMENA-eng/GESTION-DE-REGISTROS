from tkinter import messagebox
from CRUD import*
from avisos import*
class Estructura:
    
    def conexion():
        try:
            Registro.conexion()
            messagebox.showinfo("CONEXION",Avisos.EXITO_BD)
        except:
            messagebox.showinfo("CONEXION",Avisos.ERROR_BD)
    
    def eliminar():
        if messagebox.askyesno(message=Avisos.CONFIRMAR_BD, title="ADVERTENCIA"):
            Registro.eliminar()
        else:
            messagebox.showinfo("CONEXION", Avisos.ERROR_ELIMINAR_BD)
    
    def mostrar(tree):
        registros=tree.get_children()
        [tree.delete(elemento) for elemento in registros]
        try:
            asistencia=Registro.consultar()
            [tree.insert("",0, text=row[0], values=(row[1],row[2],row[3], row[4],row[5],row[6]))for row in asistencia]
        except:
            messagebox.showwarning("ADVERTENCIA",Avisos.ERROR_MOSTRAR)
    
    def consultar_dni(tree,criterio):
        registros=tree.get_children()
        [tree.delete(elemento) for elemento in registros]
        try:
            if(criterio!=""):
                asistencia=Registro.consultar_dni(criterio)
                [tree.insert("",0, text=row[0], values=(row[1],row[2],row[3], row[4],row[5],row[6])) for row in asistencia]
            else:
                messagebox.showwarning("ADVERTENCIA",Avisos.NOMBRE_FALTANTE)
        except:
            messagebox.showwarning("ADVERTENCIA", Avisos.ERROR_BUSCAR)
    
    def crear(dni,nombres,apellido_paterno,apellido_materno,genero,estado_civil):
        try:
            if(dni!="" and nombres!="" and apellido_paterno!="" and apellido_materno!="" and genero!="" and estado_civil!=""):
                Registro.crear(dni,nombres,apellido_paterno,apellido_materno,genero,estado_civil)
            else:
                pass
        except:
            pass
    
    def actualizar(dni,nombres,apellido_paterno,apellido_materno,genero,estado_civil):
        try:
            if(dni!="" and nombres!="" and apellido_paterno!="" and apellido_materno!="" and genero!="" and estado_civil!=""):
                Registro.actualizar(dni,nombres,apellido_paterno,apellido_materno,genero,estado_civil)
            else:
                messagebox.showwarning("ADVERTENCIA", Avisos.CAMPOS_FALTANTES)
        except:
            messagebox.showwarning("ADVERTENCIA", Avisos.ERROR_ACTUALIZAR)
    
    def borrar(ide):
        try:
            if messagebox.askyesno(message=Avisos.CONFIRMAR, title="ADVERTENCIA"):
                Registro.borrar(ide)
        except:
            messagebox.showwarning("ADVERTENCIA", Avisos.ERROR_ELIMINAR)
    
    def mensaje():
        messagebox.showerror(title="INFORMACION", message=Avisos.ACERCA)
    
    
                
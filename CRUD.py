import sqlite3
from base import*
from cons_asistencia import*

class Registro:
    def conectar():
        miConexion=sqlite3.connect("registro_asistencia")
        miCursor=miConexion.cursor()
        return miConexion,miCursor
    
    def conexion():
        miConexion,miCursor=Registro.conectar()
        miCursor.execute(Base.CREATE)
        return miConexion,miCursor
        
        
    def eliminar():
        miConexion,miCursor=Registro.conectar()
        miCursor.execute(Base.DELETE_TABLE)
        return miConexion,miCursor
    
    def consultar():
        miConexion,miCursor=Registro.conectar()
        miCursor.execute(Base.SELECT)
        return miConexion,miCursor
        
    def crear(dni,nombres,apellido_paterno,apellido_materno,estado_civil,genero):
        miConexion,miCursor=Registro.conectar()
        asistencia=Cons_asistencia(dni,nombres,apellido_paterno,apellido_materno,estado_civil,genero)
        miCursor.execute(Base.INSERT,(asistencia.info()))
        miConexion.commit()
    
    
    def actualizar(dni,nombres,apellido_paterno,apellido_materno,estado_civil,genero,ide):
        miConexion,miCursor=Registro.conectar()
        asistencia=Cons_asistencia(dni,nombres,apellido_paterno,apellido_materno, estado_civil,genero)
        miCursor.execute(Base.UPDATE+ide,(asistencia.info()))
        miConexion.commit()

        
    def borrar(ide):
        miconexion,miCursor=Registro.conectar()
        miCursor.execute(Base.DELETE+ide)
        miconexion.commit()
        
    def consultar_dni(dni):
        miConexion,miCursor=Registro.conectar()
        miCursor.execute(Base.BUSCAR,(dni,))
        return miConexion,miCursor
        return miCursor.fetchall()
  
    
    
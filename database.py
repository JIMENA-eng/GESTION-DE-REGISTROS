# database.py

import sqlite3

def inicializar_db():
    # Inicializar la base de datos y crear las tablas si no existen
    conn = sqlite3.connect('registro_asistencia.db')
    cursor = conn.cursor()

    # Crear tabla para administradores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS administradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Crear tabla para registros de DNI
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros_dni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT NOT NULL,
            registrado_en_api INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def registrar_admin(username, password):
    # Registrar un nuevo administrador en la base de datos
    conn = sqlite3.connect('registro_asistencia.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO administradores (username, password) VALUES (?, ?)', (username, password))

    conn.commit()
    conn.close()

def buscar_admin(username):
    # Buscar un administrador por nombre de usuario
    conn = sqlite3.connect('registro_asistencia.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM administradores WHERE username = ?', (username,))
    admin = cursor.fetchone()

    conn.close()
    return admin

def registrar_registro_dni(dni, registrado_en_api):
    # Registrar un nuevo registro de DNI en la base de datos
    conn = sqlite3.connect('registro_asistencia.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO registros_dni (dni, registrado_en_api) VALUES (?, ?)', (dni, registrado_en_api))

    conn.commit()
    conn.close()

def consultar_registro_dni(dni):
    # Consultar el registro de un DNI en la base de datos
    conn = sqlite3.connect('registro_asistencia.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM registros_dni WHERE dni = ?', (dni,))
    registro = cursor.fetchone()

    conn.close()
    return registro

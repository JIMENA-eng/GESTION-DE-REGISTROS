import tkinter as tk
from tkinter import Label, PhotoImage

# Función para cargar y mostrar una imagen
def mostrar_imagen():
    # Ruta de la imagen (ajusta la ruta según la ubicación de tu imagen)
    ruta_imagen = 'ejemplo'
    
    # Cargar la imagen
    imagen = PhotoImage(file=ruta_imagen)
    
    # Mostrar la imagen en una etiqueta
    label_imagen.config(image=imagen)
    label_imagen.image = imagen  # Mantener referencia para evitar que se elimine por el recolector de basura

# Crear la ventana principal
root = tk.Tk()
root.title("Mostrar Imagen")

# Crear etiqueta para mostrar la imagen
label_imagen = Label(root)
label_imagen.pack(padx=20, pady=20)

# Botón para mostrar la imagen
boton_mostrar = tk.Button(root, text="Mostrar Imagen", command=mostrar_imagen)
boton_mostrar.pack(pady=10)

# Ejecutar el bucle principal de la ventana
root.mainloop()
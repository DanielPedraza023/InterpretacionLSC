import os

# Directorio donde se encuentran las imágenes
directorio = 'D:/Datos/Desktop/CODIGOS/TESIS/DATA/Letra_F'  # Cambia por la ruta de tu carpeta

# Obtener la lista de archivos en el directorio
archivos = os.listdir(directorio)

# Prefijo o sufijo a añadir al nombre original de la imagen
prefijo = 'F_INVESTIGADORHUGO_'  # Puedes modificar esto como desees

# Iterar sobre los archivos en la carpeta
for i, archivo in enumerate(archivos):
    if archivo.endswith('.jpg') or archivo.endswith('.png'):  # Asegúrate de que sean archivos de imagen
        nombre_viejo = os.path.join(directorio, archivo)
      #  nombre_nuevo = os.path.join(directorio, f'{prefijo}{i}_{archivo}')  # Nuevo nombre con prefijo y número
        nombre_nuevo = os.path.join(directorio, f'{prefijo}{i}.jpg') 
        os.rename(nombre_viejo, nombre_nuevo)
        print(f"Renombrando: {nombre_viejo} a {nombre_nuevo}")

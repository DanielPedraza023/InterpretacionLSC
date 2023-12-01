import cv2

# Especifica la ruta de la imagen que deseas leer
ruta_imagen = 'D:/Copia Agosto 2022/Desktop/CODIGOS/TESIS/DATASET3/Train/P/41_P.jpg'

# Utiliza la función imread para cargar la imagen
imagen = cv2.imread(ruta_imagen)

# Verifica si la imagen se cargó correctamente
if imagen is not None:
    # La imagen se ha cargado correctamente
    # Aquí puedes realizar operaciones en la imagen si es necesario
    
    # Por ejemplo, puedes mostrar la imagen en una ventana
    cv2.imshow('Imagen', imagen)
    alto, ancho, canales = imagen.shape
    
    # Imprime las dimensiones
    print(f"Alto de la imagen: {alto} píxeles")
    print(f"Ancho de la imagen: {ancho} píxeles")
    print(f"Número de canales de color: {canales}")
    # Espera hasta que se presione una tecla y luego cierra la ventana
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    # La imagen no se pudo cargar
    print("No se pudo cargar la imagen. Verifica la ruta de la imagen.")

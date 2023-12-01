#Importar librerias
import cv2
import os

#Importar Funcion
import main 
# import Prueba2manos

#Crear carpetas con imagenes
nombre = 'Letra_ESPACIO'
direccion = 'D:/Datos/Desktop/CODIGOS/TESIS/DATAJIMMY'
carpeta = direccion + '/' + nombre 

#Si no existe la carpeta, se crea
if not os.path.exists(carpeta): 
    print("Carpeta Creada: ", carpeta)
    #Metodo para crear la carpeta
    os.makedirs(carpeta)

#Lectura de la camara
cap = cv2.VideoCapture(1) 
#Cambiar la resolucion de la captura
cap.set(3, 1280)
cap.set(4,720)

#Definir Contador
cont = 0 

#Llamar funcion de detección de manos
detector = main.detectorManos( Confdeteccion = 0.9 )
# detector = Prueba2manos.detectorManos( Confdeteccion = 0.9 )

while True:
    #Realizar lectura de Video
    ret, frame = cap.read()

    #Extraer informacion de la mano
    frame = detector.encontrarManos(frame, dibujar = False)

    #Posicion de una sola mano 
    lista1, bbox, mano = detector.encontrarPosicion(frame, ManoNum = 0, dibujarPuntos = False, dibujarBox = False , color = [255, 0, 0])
    
    #Si detecta una mano
    if mano == 1:
        #Extraer informacion del cuadro que encierra la mano
        xmin, ymin, xmax, ymax = bbox 

        #Modificamos las dimenciones del cuadro
        xmin = xmin - 60 
        ymin = ymin - 50
        xmax = xmax + 55
        ymax = ymax + 70
        print(ymin, ymax, xmin, xmax)
        if xmin < 0 or ymin < 0:
            xmin = 0
            ymin = 0
        
        #Recorte del recuadro solo con la mano 
        recorte = frame[ymin:ymax, xmin:xmax]
        
        #Guardar las imagenes
        cv2.imwrite(carpeta + "/ESPACIO_INVESTIGADORJIMMY_{}.jpg".format(cont), recorte)

        #Aumentar contador
        cont += 1
        cv2.imshow("Extraer Letra", recorte)


        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), [0, 255, 0], 2) #Recuadro Verde


    
    #Mostrar FPS
    cv2.imshow("LSC", frame)

    #Leer el teclado 
    t = cv2.waitKey(1)
    if t == 27 or cont == 120:
        break
cap.release()
cv2.destroyAllWindows()
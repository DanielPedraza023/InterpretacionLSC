#Importar librerias 
import cv2 
from ultralytics import YOLO

#Importar funcion de detección de manos 
import main 

#Lectura de la camara
cap = cv2.VideoCapture(1) 
#Cambiar la resolucion de la captura
cap.set(3, 1280)
cap.set(4,720)

#Lectura de nuestro modelo entrenado
model = YOLO("") #Colocar nombre del modelo resultante

#Llamar funcion de detección de manos
detector = main.detectorManos( Confdeteccion = 0.9 )

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
        #print(ymin, ymax, xmin, xmax) #Mostrar en pantalla la posicion del recuadro
        if xmin < 0 or ymin < 0:
            xmin = 0
            ymin = 0
        
        #Recorte del recuadro solo con la mano 
        recorte = frame[ymin:ymax, xmin:xmax]  

        #Extraer resultados del modelo 
        resultados = model.predict(recorte, conf = 0.9)  #Se crea una variable la cual almacena los resultados de las predicciones del modelo

        #Comprobar si existen resultados
        if len(resultados) != 0:
            #Iteramos en cada resultado
            for results in resultados:
                masks = results.masks
                coordenadas = masks

                anotaciones = resultados[0].plot()


        cv2.imshow("INTERPRETADOR", anotaciones)
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), [0, 255, 0], 2) #Recuadro Verde


    
    #Mostrar FPS
    cv2.imshow("LSC", frame)

    #Leer el teclado 
    t = cv2.waitKey(1)
    if t == 27:
        break
cap.release()
cv2.destroyAllWindows()
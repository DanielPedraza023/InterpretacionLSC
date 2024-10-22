#Importar librerias 
import cv2 
from ultralytics import YOLO
from TextToAudio import reproducir_audio

#Importar funcion de detección de manos 
import main 

#Lectura de la camara
cap = cv2.VideoCapture(1) 
#Cambiar la resolucion de la captura
cap.set(3, 1280)
cap.set(4,720)

#Lectura de nuestro modelo entrenado
model = YOLO("lsc.pt") #Colocar nombre del modelo resultante

#Llamar funcion de detección de manos
detector = main.detectorManos( Confdeteccion = 0.9 )

#Lista que guarda las señales reconocidas
señales_reconocidas = []
señal_en_imagen = []
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

        #Redimensionar 
        #recorte = cv2.resize(recorte, (640, 640), interpolation = cv2.INTER_CUBIC)

        #Extraer resultados del modelo 
        resultados = model.predict(recorte, conf = 0.55)  #Se crea una variable la cual almacena los resultados de las predicciones del modelo

        #Comprobar si existen resultados
        if len(resultados) != 0:
            #Señales en la imagen 
            señal_en_imagen = []

            #Iteramos en cada resultado
            for results in resultados:
                masks = results.masks
                coordenadas = masks

                anotaciones = resultados[0].plot()

                #Obtener clase de la señal
                clase = results.names[0]

                # Agregar la clase de la señal a la lista de señales únicas si no está ya presente
                if clase not in señal_en_imagen:
                    señal_en_imagen.append(clase)


                señal_en_imagen.append(clase)
            
            señales_reconocidas.append(señal_en_imagen)

        cv2.imshow("INTERPRETADOR", anotaciones)
        #cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), [0, 255, 0], 2) #Recuadro Verde


    
    #Mostrar FPS
    cv2.imshow("LSC", frame)

    #Leer el teclado 
    t = cv2.waitKey(1)

    if t == 27:
        break
    
    elif t == 13:
        if not señales_reconocidas:
            print("No se ha detectado ninguna señal")
            reproducir_audio("No se ha detectado ninguna señal")
        
        else:
            # Convertir cada lista de señales en una cadena
            palabras = []
            
            for señales in señales_reconocidas:
                palabra_actual = ''
                for señal in señales:
                    if señal == 'ESPACIO':
                        palabra_actual += ' '  # Agregar espacio si la señal es "ESPACIO"
                    else:
                        palabra_actual += señal
                palabras.append(palabra_actual)
            # Unir todas las palabras en una sola cadena
            palabra_completa = ''.join(palabras)

            print("Palabra completa formada por las señales reconocidas:", palabra_completa)
            reproducir_audio( palabra_completa)

        señales_reconocidas = []
        señal_en_imagen = []

    # else:
    #     # Agregamos las señales únicas de la imagen actual a la lista general
    #     señales_reconocidas.append(señal_en_imagen)

cap.release()
cv2.destroyAllWindows()
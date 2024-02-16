#Paso 1: 
#pip install labelme, pip install mediapipe --> terminal

#Paso 2 importar librerias
import cv2
import mediapipe as mp

#Se crea una clase
class detectorManos():

    #Inicializar parametros de la deteccion
    def __init__(self, mode = False, maxManos = 2, model_complexity = 1, Confdeteccion = 0.5, confsegui = 0.5):
        self.mode = mode  #Se crea el objeto el cual tendrá su propia variable
        self.maxManos = maxManos #Lo mismo se hará con los objetos
        self.compl = model_complexity
        self.Confdeteccion = Confdeteccion
        self.confsegui = confsegui 
    
        #Crear objetos que detectan manos y las dibujan
        self.mpmanos = mp.solutions.hands
        self.manos = self.mpmanos.Hands(self.mode, self.maxManos, self.compl, self.Confdeteccion, self.confsegui)
        self.dibujo = mp.solutions.drawing_utils
        self.tip = [4, 8, 12, 16, 20]

    #Funcion para encontrar manos
    def encontrarManos(self, frame, dibujar = False): #Se define la funcion con sus parametros. self -> instancia de la clase  / frame -> imagen recibida  / dibujar -> opcion de dibujar los puntos claves
        imgcolor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Conversion de color de la imagen leida. Cuando opencv lee una imagen la convierte a BGR. Mediapipe espera que la imagen esté en RBG, por eso es necesaria la conversion
        self.resultados = self.manos.process(imgcolor) #Realiza la deteccion de manos en la imagen convertida a RBG (imgcolor). La respuesta se guarda en "self.resultados"
        if self.resultados.multi_hand_landmarks: #Verifica si se han detectados manos
            for mano in self.resultados.multi_hand_landmarks: # Inicia un bucle que recorre cada mano detectada en el Frame. self.resultados.multi_hand_landmarks -> es una lista que contiene los puntos claves de la mano detectada
                if dibujar: #Si el parametro de la funcion es True procede a dibujar los puntos claves de las manos detectadas 
                    self.dibujo.draw_landmarks(frame, mano, self.mpmanos.HAND_CONNECTIONS) #Funcion de mediapipe que se encarga de la conexion de los puntos claves de la mano
        return frame #Devuelve el frame con los puntos claves de las manos detectadas, dependiendo del parametro inicial de la funcion
    
    #Funcion para encontrar la posicion de la mano detectada
    def encontrarPosicion(self, frame, ManoNum = 0, dibujarPuntos = True, dibujarBox = True, color = []): 
        xlista = []
        ylista = []
        bbox = []
        player = 0
        self.lista = []
        if self.resultados.multi_hand_landmarks: #Verifica si se ha detectado alguna mano. Si no se detecta ninguna mano no se ejecuta el bloque siguiente
            #Se accede a la informacion de la mano detectada
            miMano = self.resultados.multi_hand_landmarks[ManoNum] #Se accede la mano que se especifica en el parametro ManoNum
            prueba = self.resultados.multi_hand_landmarks
            player = len(prueba) #Obtiene el numero total de manos detectadas
            for id, lm in enumerate(miMano.landmark): #Bucle que recorre los puntos claves de la mano detectada
                alto, ancho, c = frame.shape #Extraemos las dimensiones de los fps 
                cx, cy = int(lm.x * ancho), int(lm.y * alto) #Convertimos la informacion en pixeles. Calcula la posicion de cada punto clave de la mano en pixeles utilizando la coordenadas normalizadas (lm.x, lm.y) proporcionadas por mediapipe
                xlista.append(cx) #Almecena las coordenadas en x
                ylista.append(cy) #Almacena las coordenadas en y
                self.lista.append([id, cx, cy]) #Se agrega informacion del punto clave
                if dibujarPuntos: #Si dibujarPuntos = True, dibuja un pequeño circulo en el punto clave del frame
                    cv2.circle(frame, (cx, cy), 3, (0, 0, 0), cv2.FILLED) #Dibujamos un circulo 
            xmin, xmax = min(xlista), max(xlista) #Toma los valores maximos y minimos en x para dibujar el cuadro que rodea la mano detectada 
            ymin, ymax = min(ylista), max(ylista)
            bbox = xmin, ymin, xmax, ymax 
            if dibujarBox: #Si el parametro dibujarbox = True, dibuja un cuadro alrededor de la mano detectada
                #Dibujamos cuadro 
                cv2.rectangle(frame, (xmin - 10, ymin - 40), (xmax + 40, ymax + 40), color, 2) #Dibuja el cuadro alrededor de la mano, la variable color depende del parametro inicial de la funcion
        return self.lista, bbox, player # Devuelve: self.lista -> informacion de los puntos claves de la mano / bbox -> coordenadas del cuadro que encierra la mano  / player -> numero total de manos detectadas

    #Funcion para detectar los dedos arriba
    def dedosArriba(self): #self -> instacia de la clase
        dedos = [] #Para llevar la cuenta de cuantos dedos están levantados
        if self.lista[self.tip[0]][1] > self.lista[self.tip[0] - 1][1]:
            dedos.append(1)
        else:
            dedos.append(0)

        for id in range (1,5):
            if self.lista[self.tip[id]][2] < self.lista[self.tip[id] - 2][2]:
                dedos.append(1)
            else:
                dedos.append(0)
        return dedos





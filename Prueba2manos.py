import cv2
import mediapipe as mp
import time  

class detectorManos():

    def __init__(self, mode=False, maxManos=2, model_complexity=1, Confdeteccion=0.5, confsegui=0.5):
        self.mode = mode
        self.maxManos = maxManos
        self.compl = model_complexity
        self.Confdeteccion = Confdeteccion
        self.confsegui = confsegui

        self.mpmanos = mp.solutions.hands
        self.manos = self.mpmanos.Hands(self.mode, self.maxManos, self.compl, self.Confdeteccion, self.confsegui)
        self.dibujo = mp.solutions.drawing_utils
        self.tip = [4, 8, 12, 16, 20]

    def encontrarManos(self, frame, dibujar=True):
        imgcolor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.resultados = self.manos.process(imgcolor)

        if self.resultados.multi_hand_landmarks:
            for mano in self.resultados.multi_hand_landmarks:
                if dibujar:
                    self.dibujo.draw_landmarks(frame, mano, self.mpmanos.HAND_CONNECTIONS)

        return frame

    def encontrarPosicion(self, frame, ManoNum=0, dibujarPuntos=True, dibujarBox=True, color=[]):
        xlista = []
        ylista = []
        bbox = []
        player = 0
        self.lista = []

        if self.resultados.multi_hand_landmarks:
            player = len(self.resultados.multi_hand_landmarks)

            for i, mano in enumerate(self.resultados.multi_hand_landmarks):
                xlista = []
                ylista = []

                for id, lm in enumerate(mano.landmark):
                    alto, ancho, c = frame.shape
                    cx, cy = int(lm.x * ancho), int(lm.y * alto)
                    xlista.append(cx)
                    ylista.append(cy)
                    self.lista.append([id, cx, cy])

                    if dibujarPuntos:
                        cv2.circle(frame, (cx, cy), 3, (0, 0, 0), cv2.FILLED)

                xmin, xmax = min(xlista), max(xlista)
                ymin, ymax = min(ylista), max(ylista)
                bbox.append((xmin - 10, ymin - 40, xmax + 40, ymax + 40))

                if dibujarBox:
                    cv2.rectangle(frame, (xmin - 10, ymin - 40), (xmax + 40, ymax + 40), color[i], 2)

        return self.lista, bbox, player

    def dedosArriba(self):
        dedos = []

        for i in range(len(self.resultados.multi_hand_landmarks)):
            if self.lista[self.tip[0]][1] > self.lista[self.tip[0] - 1][1]:
                dedos.append(1)
            else:
                dedos.append(0)

            for id in range(1, 5):
                if self.lista[self.tip[id]][2] < self.lista[self.tip[id] - 2][2]:
                    dedos.append(1)
                else:
                    dedos.append(0)

        return dedos


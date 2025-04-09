"""
Detección de Manos en Tiempo Real

Este script utiliza OpenCV y la biblioteca cvzone para detectar manos en tiempo real a través de la cámara web.
Se detectan los puntos clave (landmarks) de la mano y se dibujan sobre el video en vivo.
"""

import cv2
from cvzone.HandTrackingModule import HandDetector

# Inicializar el detector de manos
# detectionCon: Nivel de confianza para la detección (0.5 por defecto)
# maxHands: Número máximo de manos a detectar (1 en este caso)
detector = HandDetector(detectionCon=0.5, maxHands=1)

# Iniciar la captura de video desde la cámara web
cap = cv2.VideoCapture(0)

while True:
    # Leer un frame de la cámara
    success, img = cap.read()

    # Verificar si el frame se capturó correctamente
    if not success:
        print("Error al capturar el video")
        break

    # Detectar manos en el frame
    # findHands devuelve una lista de manos detectadas y la imagen con los landmarks dibujados (si se habilita)
    hands, img = detector.findHands(img)  # Sin dibujar landmarks automáticamente

    # Si se detectan manos
    if hands:
        # Obtener la primera mano detectada
        hand = hands[0]

        # Obtener la lista de puntos clave (landmarks) de la mano
        lmList = hand['lmList']  # Lista de puntos clave [(x, y, z), ...]

        # Dibujar los puntos clave en la imagen
        for lm in lmList:
            cv2.circle(img, (lm[0], lm[1]), 5, (255, 0, 0), cv2.FILLED)

    # Mostrar la imagen con los puntos clave dibujados
    cv2.imshow("Mano detectada", img)

    # Esperar 1ms y salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
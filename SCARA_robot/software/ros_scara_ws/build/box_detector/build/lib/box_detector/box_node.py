import cv2

def main():
    print('Hi from box_detector.')

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
    else:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar imagen")
        else:
            print("Cámara funcionando correctamente")
        cap.release()

if __name__ == '__main__':
    main()

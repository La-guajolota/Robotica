import cv2

# Modificar índice de la función para cambiar entre cámaras
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

if not cap.isOpened():
    print("Error al abrir la cámara")
else:
    while True:
        # Capturar el fotograma
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el fotograma")
            break

        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Suavizar la imagen
        smooth_img = cv2.medianBlur(gray, 31)

        # Aplicar umbral binario inverso
        _, bin_img = cv2.threshold(smooth_img, 50, 254, cv2.THRESH_BINARY_INV)

        # Detectar bordes
        edges = cv2.Canny(bin_img, 10, 40)

        # Encontrar contornos
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Procesar cada contorno
        for contour in contours:
            perimetro = cv2.arcLength(contour, True)
            epsilon = 0.16 * perimetro
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Verificar si el contorno tiene 4 lados (rectángulo)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                cv2.putText(frame, f'Position:({x},{y})', (x + 50, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Mostrar las imágenes procesadas
        cv2.imshow("Escal de grises",gray)
        cv2.imshow("Imagen Suavizada", smooth_img)
        cv2.imshow("Imagen Binaria", bin_img)
        cv2.imshow("Forma Encontrada", frame)

        # Salir al presionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
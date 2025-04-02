import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen en modo color
image_path = "vision/btns2.png"  # Cambia esto por la ruta de tu imagen
image = cv2.imread(image_path, cv2.IMREAD_COLOR)

# Verificar si la imagen se cargó correctamente
if image is None:
    raise FileNotFoundError(f"No se pudo cargar la imagen en {image_path}")

# Convertir a escala de grises
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar un filtro Gaussiano para reducir el ruido
# con un kernel de 5x5 para suavizar la imagen y reducir el ruido
blurred_image = cv2.GaussianBlur(gray_image, (3,3), 0)

# Aplicar umbralización para segmentar los círculos negros
_, binary_image = cv2.threshold(blurred_image, 71, 255, cv2.THRESH_BINARY_INV)

# Encontrar contornos en la imagen binaria
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filtrar contornos por forma (circularidad)
detected_circles = []
for contour in contours:
    # Calcular el área y el perímetro del contorno
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    
    if perimeter == 0:  # Evitar divisiones por cero
        continue
    
    # Calcular circularidad: (4 * π * área) / (perímetro^2)
    circularity = (4 * np.pi * area) / (perimeter ** 2)
    
    # Filtrar por área mínima y circularidad cercana a 1 (círculos)
    if area > 50 and 0.7 < circularity <= 1.2:
        detected_circles.append(contour)

# Dibujar los círculos detectados en la imagen original
output_image = image.copy()
cv2.drawContours(output_image, detected_circles, -1, (0, 255, 0), 2)

# Mostrar la imagen original con los círculos detectados
plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
plt.title("Círculos Detectados")
plt.show()

# Mostrar la imagen binaria para referencia
plt.imshow(binary_image, cmap='gray')
plt.title("Imagen Binaria")
plt.show()



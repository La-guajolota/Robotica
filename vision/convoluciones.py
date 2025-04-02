import cv2
import numpy as np
from scipy.ndimage import gaussian_filter, sobel, prewitt, laplace, median_filter
import matplotlib.pyplot as plt

# Cargar la imagen en escala de grises
image_path = "vision/btns0.jpeg"  # Cambia esto por la ruta de tu imagen
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Verificar si la imagen se cargó correctamente
if image is None:
    raise FileNotFoundError(f"No se pudo cargar la imagen en {image_path}")

# Aplicar filtros
average = cv2.blur(image, (5, 5))  # Filtro promedio
gaussian = gaussian_filter(image, sigma=1)  # Filtro Gaussiano
sobel_x = sobel(image, axis=0)  # Sobel en X
sobel_y = sobel(image, axis=1)  # Sobel en Y
sobel_combined = np.hypot(sobel_x, sobel_y)  # Magnitud combinada de Sobel
prewitt_x = prewitt(image, axis=0)  # Prewitt en X
prewitt_y = prewitt(image, axis=1)  # Prewitt en Y
prewitt_combined = np.hypot(prewitt_x, prewitt_y)  # Magnitud combinada de Prewitt
laplacian = laplace(image)  # Filtro Laplaciano
highpass = image - gaussian  # Filtro pasa-altas
median = median_filter(image, size=3)  # Filtro Mediano
min_filter = cv2.erode(image, np.ones((3, 3), np.uint8))  # Filtro Mínimo
max_filter = cv2.dilate(image, np.ones((3, 3), np.uint8))  # Filtro Máximo
bilateral = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)  # Filtro Bilateral

# Crear un diccionario con los filtros
filters = {
    "Original": image,
    "Average": average,
    "Gaussian": gaussian,
    "Sobel": sobel_combined,
    "Prewitt": prewitt_combined,
    "Laplace": laplacian,
    "Highpass": highpass,
    "Median": median,
    "Min": min_filter,
    "Max": max_filter,
    "Bilateral": bilateral,
}

# Mostrar las imágenes una por una
for name, filtered_image in filters.items():
    plt.figure(figsize=(8, 6))
    plt.imshow(filtered_image, cmap="gray")
    plt.title(f"{name} - Imagen")
    plt.axis("off")
    plt.show()

plt.tight_layout()
plt.show()
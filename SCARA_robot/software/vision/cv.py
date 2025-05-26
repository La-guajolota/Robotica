import cv2
import numpy as np
import pandas as pd

# Ruta de la imagen a procesar
image_path = input("Ingrese la ruta de la imagen: ")

# Leer la imagen
image = cv2.imread(image_path)
if image is None:
    print("Error: No se pudo leer la imagen. Verifique la ruta y el archivo.")
    exit()

# Convertir a escala de grises y aplicar desenfoque
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)

# Encontrar contornos
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Convertir la imagen a RGB para dibujar contornos
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Constante de conversión de píxeles a centímetros
PIXELS_PER_CM = 10.0

results = []

for i, c in enumerate(contours):
    if cv2.contourArea(c) < 100:
        continue

    rect = cv2.minAreaRect(c)
    (x, y), (w, h), angle = rect

    if w == 0 or h == 0:
        continue

    width_cm = round(w / PIXELS_PER_CM, 2)
    height_cm = round(h / PIXELS_PER_CM, 2)

    box = cv2.boxPoints(rect)
    box = np.intp(box)
    cv2.drawContours(image_rgb, [box], 0, (0, 255, 0), 2)

    results.append({
        "Object #": i + 1,
        "Width (cm)": max(width_cm, height_cm),
        "Height (cm)": min(width_cm, height_cm),
        "Area (cm²)": round(width_cm * height_cm, 2)
    })

# Mostrar la imagen con los contornos dibujados
cv2.imshow("Measured Objects", cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))
cv2.waitKey(0)
cv2.destroyAllWindows()

# Generar reporte si hay resultados
if results:
    df = pd.DataFrame(results)
    print("\n📄 Measurement Report:")
    print(df)

    # Guardar el reporte en un archivo CSV
    output_csv = "measurement_report.csv"
    # df.to_csv(output_csv, index=False)
    print(f"\n📥 Reporte guardado como: {output_csv}")
else:
    print("No se detectaron objetos medibles en la imagen.")
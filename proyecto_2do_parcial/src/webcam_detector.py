"""
smoker_detector_webcam.py
Este script utiliza un modelo de aprendizaje profundo para detectar si una persona está fumando en tiempo real
usando la webcam. El modelo previamente entrenado se carga y se utiliza para realizar predicciones en cada
frame capturado por la cámara. La salida incluye información visual sobre la predicción, confianza, FPS y
tiempo de inferencia.
Autor: Adrián Silva Palafox y Felipe Adriel Trejo De Arcos 
Fecha: 2023-27-05
Funciones:
-----------
preprocess_image(img, target_size):
    Preprocesa una imagen para que sea compatible con el modelo de predicción.
    - Redimensiona la imagen al tamaño objetivo.
    - Normaliza los valores de los píxeles entre 0 y 1.
    - Añade una dimensión de lote para que sea compatible con el modelo.
main():
    Función principal que ejecuta el flujo del programa.
    - Carga el modelo de detección de fumadores desde un archivo .h5.
    - Inicializa la webcam para capturar video en tiempo real.
    - Procesa cada frame capturado para realizar predicciones.
    - Muestra los resultados en tiempo real, incluyendo:
        - Estado de detección ("FUMANDO" o "NO FUMANDO").
        - Nivel de confianza de la predicción.
        - FPS (frames por segundo) del procesamiento.
        - Tiempo de inferencia del modelo en milisegundos.
    - Permite salir del programa presionando la tecla 'q'.
Variables y constantes:
------------------------
MODEL_PATH : str
    Ruta al archivo del modelo preentrenado (.h5).
IMG_SIZE : tuple
    Tamaño de las imágenes de entrada esperado por el modelo (ancho, alto).
cap : cv2.VideoCapture
    Objeto para capturar video desde la webcam.
fps_start_time : float
    Marca de tiempo inicial para calcular FPS.
fps_frame_count : int
    Contador de frames procesados para calcular FPS.
fps : float
    Frames por segundo calculados.
threshold : float
    Umbral para clasificar si alguien está fumando o no.
Dependencias:
-------------
- cv2 (OpenCV): Para capturar video y mostrar resultados visuales.
- numpy: Para manipulación de datos numéricos.
- tensorflow.keras: Para cargar el modelo de aprendizaje profundo.
- time: Para medir tiempos de procesamiento y calcular FPS.
Uso:
----
1. Asegúrate de tener un modelo entrenado guardado en la ruta especificada por `MODEL_PATH`.
2. Conecta una webcam al sistema.
3. Ejecuta el script desde la terminal o un entorno de desarrollo.
4. Observa los resultados en tiempo real en la ventana de video.
5. Presiona 'q' para salir del programa.
Notas:
------
- Asegúrate de que el modelo cargado sea compatible con las dimensiones de entrada especificadas por `IMG_SIZE`.
- Si la webcam no se abre correctamente, verifica el índice de la cámara en `cv2.VideoCapture(2)` y cámbialo si es necesario.
- El script está diseñado para funcionar con modelos binarios que predicen si alguien está fumando o no.
"""
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import time

# Configurar TensorFlow para usar la GPU
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    print(f"GPUs detectadas: {len(physical_devices)}")
    for device in physical_devices:
        tf.config.experimental.set_memory_growth(device, True)
else:
    print("No se detectaron GPUs. TensorFlow usará la CPU.")

def preprocess_image(img, target_size):
    """Preprocesa una imagen para la predicción"""
    img = cv2.resize(img, target_size)
    img = img / 255.0  # Normalizar
    img = np.expand_dims(img, axis=0)  # Añadir dimensión de lote
    return img

def main():
    # Configuración
    MODEL_PATH = "models/smoking_detector_model.h5"
    IMG_SIZE = (224, 224)  # Mismo tamaño usado durante el entrenamiento
    
    # Cargar modelo entrenado
    print("Cargando modelo...")
    model = load_model(MODEL_PATH)
    print("¡Modelo cargado!")
    
    # Inicializar webcam
    print("Iniciando webcam...")
    cap = cv2.VideoCapture(2)  # 0 para webcam predeterminada
    
    # Verificar si la webcam se abrió correctamente
    if not cap.isOpened():
        print("Error: No se pudo abrir la webcam.")
        return
    
    # Variables para calcular FPS
    fps_start_time = time.time()
    fps_frame_count = 0
    fps = 0
    
    print("Presiona 'q' para salir")
    
    while True:
        # Capturar frame
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo capturar el frame.")
            break
        
        # Crear copia para visualización
        display_frame = frame.copy()
        
        # Preprocesar frame para predecir
        processed_frame = preprocess_image(frame, IMG_SIZE)
        
        # Realizar predicción
        start_time = time.time()
        prediction = model.predict(processed_frame, verbose=0)[0][0]
        inference_time = (time.time() - start_time) * 1000  # en ms
        
        # Calcular FPS
        fps_frame_count += 1
        if (time.time() - fps_start_time) > 1:
            fps = fps_frame_count / (time.time() - fps_start_time)
            fps_frame_count = 0
            fps_start_time = time.time()
        
        # Determinar resultado
        threshold = 0.85 # Umbral de confianza
        result = "FUMANDO" if prediction > threshold else "NO FUMANDO" 
        confidence = prediction if prediction > threshold else 1 - prediction
        color = (0, 0, 255) if prediction > threshold else (0, 255, 0)
        
        # Mostrar información en pantalla
        cv2.putText(display_frame, f"Predicción: {result}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(display_frame, f"Confianza: {confidence:.2f}", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, 110), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 165, 0), 2)
        cv2.putText(display_frame, f"Tiempo: {inference_time:.1f}ms", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 165, 0), 2)
        
        # Mostrar frame
        cv2.imshow('Detector de Fumadores', display_frame)
        
        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
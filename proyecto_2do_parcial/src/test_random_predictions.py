"""
test_random_pictures.py
Este script utiliza un modelo de aprendizaje profundo previamente entrenado para realizar predicciones 
sobre imágenes seleccionadas aleatoriamente de un conjunto de prueba. El modelo clasifica las imágenes 
en dos categorías: fumando y no fumando.

Autor: Adrián Silva Palafox y Felipe Adriel Trejo De Arcos 
Fecha: 2023-27-05

Funciones principales:
- Cargar un modelo previamente entrenado desde un archivo.
- Seleccionar aleatoriamente imágenes del conjunto de prueba.
- Preprocesar las imágenes para que sean compatibles con el modelo.
- Realizar predicciones sobre las imágenes seleccionadas.
- Mostrar las imágenes junto con las predicciones, etiquetas reales y confianza del modelo.

Parámetros:
- MODEL_PATH: Ruta al archivo del modelo entrenado (formato .h5).
- TEST_DIR: Directorio que contiene las imágenes de prueba organizadas en subdirectorios por clase.
- num_samples: Número de imágenes aleatorias a seleccionar para realizar predicciones.

Salida:
- Ventana gráfica que muestra las imágenes seleccionadas, sus predicciones, etiquetas reales y confianza.
- Las imágenes se muestran con un borde verde si la predicción es correcta y rojo si es incorrecta.

Requisitos:
- TensorFlow y Keras.
- OpenCV para procesamiento de imágenes.
- Matplotlib para visualización.
- Estructura de directorios adecuada con imágenes organizadas en carpetas por clase.

Nota:
Asegúrate de que las imágenes de prueba estén organizadas en subdirectorios dentro de la carpeta de prueba, 
con nombres de subdirectorios que correspondan a las clases (por ejemplo, "smoking" y "not_smoking").
"""
import os
import random
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import cv2

def load_and_preprocess_image(img_path, target_size=(224, 224)):
    """Carga y preprocesa una imagen para predicción"""
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convertir de BGR a RGB
    img_resized = cv2.resize(img, target_size)
    img_array = np.expand_dims(img_resized / 255.0, axis=0)  # Normalizar y añadir dimensión de lote
    return img, img_resized, img_array

def show_random_predictions(model_path, test_dir, num_samples=5):
    """Muestra predicciones para un número aleatorio de imágenes de prueba"""
    # Cargar el modelo
    print("Cargando modelo...")
    model = load_model(model_path)
    print("Modelo cargado correctamente")
    
    # Obtener rutas de imágenes de prueba
    smoking_dir = os.path.join(test_dir, "smoking")
    not_smoking_dir = os.path.join(test_dir, "not_smoking")
    
    smoking_files = [os.path.join(smoking_dir, f) for f in os.listdir(smoking_dir) 
                     if os.path.isfile(os.path.join(smoking_dir, f)) and 
                     f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    not_smoking_files = [os.path.join(not_smoking_dir, f) for f in os.listdir(not_smoking_dir) 
                         if os.path.isfile(os.path.join(not_smoking_dir, f)) and 
                         f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Combinar y mezclar las imágenes
    all_files = smoking_files + not_smoking_files
    random.shuffle(all_files)
    
    # Seleccionar un subconjunto aleatorio
    selected_files = all_files[:num_samples] if len(all_files) >= num_samples else all_files
    
    # Preparar la visualización
    plt.figure(figsize=(15, 10))
    
    for i, img_path in enumerate(selected_files):
        # Cargar y preprocesar imagen
        original_img, _, img_array = load_and_preprocess_image(img_path)
        
        # Realizar predicción
        prediction = model.predict(img_array, verbose=0)[0][0]
        
        # Determinar la etiqueta real basada en la ruta
        true_label = "Fumando" if "smoking" in img_path.split(os.sep)[-2] else "No Fumando"
        
        # Determinar la etiqueta predicha
        pred_label = "Fumando" if prediction > 0.5 else "No Fumando"
        
        # Determinar si la predicción es correcta
        is_correct = (true_label == pred_label)
        border_color = 'green' if is_correct else 'red'
        
        # Calcular confianza
        confidence = prediction if prediction > 0.5 else 1 - prediction
        
        # Mostrar la imagen con resultados
        plt.subplot(1, num_samples, i+1)
        plt.imshow(original_img)
        plt.title(f"Predicción: {pred_label}\nReal: {true_label}\nConfianza: {confidence:.2f}", 
                  color=border_color)
        plt.axis('off')
        
        # Añadir un borde de color para indicar predicción correcta/incorrecta
        plt.gca().spines['top'].set_color(border_color)
        plt.gca().spines['bottom'].set_color(border_color)
        plt.gca().spines['left'].set_color(border_color)
        plt.gca().spines['right'].set_color(border_color)
        for spine in plt.gca().spines.values():
            spine.set_linewidth(5)
    
    plt.tight_layout()
    plt.suptitle("Predicciones del Modelo de Detección de Fumadores", fontsize=16, y=1.05)
    plt.show()

if __name__ == "__main__":
    # Configurar rutas
    MODEL_PATH = "models/smoking_detector_model.h5"
    TEST_DIR = "data/processed/test"
    
    # Mostrar predicciones aleatorias
    show_random_predictions(MODEL_PATH, TEST_DIR, num_samples=5)
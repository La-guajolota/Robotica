"""
    train_model.py
    Este script entrena un modelo de aprendizaje profundo utilizando transferencia de aprendizaje con MobileNetV2 
    para clasificar imágenes en dos categorías (por ejemplo, fumando vs no fumando). El modelo se entrena con 
    imágenes preprocesadas y se guarda el mejor modelo basado en la precisión de validación.
    Autor: Adrián Silva Palafox y Felipe Adriel Trejo De Arcos 
    Fecha: 2023-27-05
    Funciones principales:
    - Configuración de rutas de datos y parámetros de entrenamiento.
    - Preparación de generadores de datos con aumento de datos para entrenamiento, validación y prueba.
    - Creación de un modelo de transferencia de aprendizaje basado en MobileNetV2.
    - Entrenamiento del modelo con un callback para guardar el mejor modelo.
    - Evaluación del modelo en el conjunto de prueba.
    - Visualización y guardado de las gráficas de precisión y pérdida durante el entrenamiento.
    Parámetros:
    - DATA_DIR: Directorio raíz donde se encuentran los datos procesados.
    - TRAIN_DIR, VALIDATION_DIR, TEST_DIR: Subdirectorios para datos de entrenamiento, validación y prueba.
    - IMG_SIZE: Tamaño al que se redimensionan las imágenes (224x224 píxeles).
    - BATCH_SIZE: Tamaño del lote para el entrenamiento.
    - EPOCHS: Número de épocas para el entrenamiento.
    - MODEL_SAVE_PATH: Ruta donde se guarda el modelo entrenado.
    Salida:
    - Modelo entrenado y guardado en la ruta especificada.
    - Gráficas de precisión y pérdida guardadas en el directorio "models/plots".
    - Precisión del modelo en el conjunto de prueba mostrada en consola.
    Requisitos:
    - TensorFlow y Keras.
    - Matplotlib para visualización.
    - Estructura de directorios adecuada con imágenes organizadas en carpetas por clase.
    Nota:
    Asegúrate de que las imágenes estén organizadas en subdirectorios dentro de las carpetas de entrenamiento, 
    validación y prueba, con nombres de subdirectorios que correspondan a las clases.

"""

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
import os
import datetime

# Configurar rutas de datos [según el arbol de directorios]
DATA_DIR = "data/processed"
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VALIDATION_DIR = os.path.join(DATA_DIR, "validation")
TEST_DIR = os.path.join(DATA_DIR, "test")

# Parámetros
IMG_SIZE = 224  # Tamaño de las imágenes (224x224 píxeles)
BATCH_SIZE = 100  # Número de imágenes procesadas en cada iteración
EPOCHS = 100  # Número de veces que el modelo verá todo el conjunto de datos
MODEL_SAVE_PATH = "models/smoking_detector_model.h5"

# Asegurarse de que existe el directorio para guardar el modelo
os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

# Preparar generadores de datos con aumento de datos
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# Cargar datos de entrenamiento
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

# Cargar datos de validación
validation_generator = validation_datagen.flow_from_directory(
    VALIDATION_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

# Cargar datos de prueba
test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

print(f"Clases encontradas: {train_generator.class_indices}")

# Crear modelo con MobileNetV2 como base (transfer learning)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))

# Congelar el modelo base
base_model.trainable = False

# Añadir capas personalizadas
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(1, activation='sigmoid')(x)  # Salida binaria (fumando vs no fumando)

model = Model(inputs=base_model.input, outputs=predictions)

# Compilar modelo
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Resumen del modelo
model.summary()

# Crear callback para guardar el mejor modelo
checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=MODEL_SAVE_PATH,
    save_best_only=True,
    monitor='val_accuracy',
    mode='max',
    verbose=1
)

# Entrenar modelo
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE,
    callbacks=[checkpoint_callback]
)

# Evaluar en conjunto de prueba
test_loss, test_accuracy = model.evaluate(test_generator)
print(f"Precisión en el conjunto de prueba: {test_accuracy:.4f}")

# Guardar historial de entrenamiento
plt.figure(figsize=(12, 4))

# Gráfica de precisión
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Entrenamiento')
plt.plot(history.history['val_accuracy'], label='Validación')
plt.title('Precisión del modelo')
plt.ylabel('Precisión')
plt.xlabel('Época')
plt.legend()

# Gráfica de pérdida
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Entrenamiento')
plt.plot(history.history['val_loss'], label='Validación')
plt.title('Pérdida del modelo')
plt.ylabel('Pérdida')
plt.xlabel('Época')
plt.legend()

# Guardar gráficas
os.makedirs("models/plots", exist_ok=True)
plt.savefig("models/plots/training_history.png")
plt.show()

print(f"Entrenamiento completado. Modelo guardado en {MODEL_SAVE_PATH}")
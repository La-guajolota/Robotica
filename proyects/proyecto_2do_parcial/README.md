# 🚭 Detector de Fumadores con IA

Un sistema de detección en tiempo real que identifica si una persona está fumando (cigarrillo convencional o vaper) utilizando visión por computadora y aprendizaje profundo.

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Conjunto de Datos](#conjunto-de-datos)
- [Entrenamiento del Modelo](#entrenamiento-del-modelo)
- [Evaluación y Pruebas](#evaluación-y-pruebas)
- [Detección en Tiempo Real](#detección-en-tiempo-real)
- [Implementación en Hardware Limitado](#implementación-en-hardware-limitado)
- [Resultados](#resultados)
- [Mejoras Futuras](#mejoras-futuras)
- [Licencia](#licencia)

## 🔍 Descripción General

Este proyecto implementa un sistema de visión por computadora capaz de detectar en tiempo real si una persona está fumando. Utiliza técnicas de aprendizaje profundo (deep learning) mediante transfer learning con el modelo MobileNetV2 preentrenado, optimizado para ejecutarse tanto en computadoras convencionales como en dispositivos de recursos limitados (como Raspberry Pi o Milk-V Duo).

### Aplicaciones Potenciales

- Monitoreo de zonas libres de humo
- Aplicaciones de salud y bienestar
- Vigilancia en entornos controlados
- Estudios sobre hábitos de consumo de tabaco

## 📁 Estructura del Proyecto

```
smoking_detection_project/
│
├── data/
│   ├── raw/                    # Imágenes sin procesar
│   │   ├── smoking/            # Personas fumando
│   │   └── not_smoking/        # Personas no fumando
│   │
│   └── processed/              # Imágenes organizadas para entrenamiento
│       ├── train/
│       │   ├── smoking/
│       │   └── not_smoking/
│       ├── validation/
│       │   ├── smoking/
│       │   └── not_smoking/
│       └── test/
│           ├── smoking/
│           └── not_smoking/
│
├── models/                     # Modelos entrenados y convertidos
│   ├── smoking_detector_model.h5        # Modelo principal
│   ├── smoking_detector_tflite.tflite   # Modelo optimizado para dispositivos
│   └── plots/                  # Gráficas de entrenamiento
│
├── src/                        # Código fuente
│   ├── organize_images.py      # Script para organizar imágenes
│   ├── split_dataset.py        # Script para dividir el conjunto de datos
│   ├── train_model.py          # Script de entrenamiento
│   ├── webcam_detector.py      # Aplicación de detección en tiempo real
│   └── test_random_predictions.py  # Evaluación con imágenes aleatorias
│
├── raspberry_pi/               # Implementación para Raspberry Pi
│   └── smoking_detector_rpi.py # Script optimizado para Raspberry
│
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

## 💻 Requisitos

- Python 3.7+
- TensorFlow 2.4+
- OpenCV 4.5+
- NumPy
- Matplotlib
- Webcam compatible (para detección en tiempo real)

Para instalar todas las dependencias:

```bash
pip install -r requirements.txt
```

## 🛠 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/username/smoking-detection.git
cd smoking-detection
```

2. Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

3. Crea la estructura de carpetas del proyecto:
```bash
mkdir -p data/raw/smoking data/raw/not_smoking data/processed models/plots
```

## 📊 Conjunto de Datos

El proyecto utiliza un conjunto de datos categorizado en dos clases:

1. **Clase "Fumando"**: Personas fumando cigarrillos convencionales o usando vapers
2. **Clase "No fumando"**: Personas realizando actividades similares (comiendo, mordiendo objetos, bebiendo, etc.)

### Organización de Imágenes

Para organizar imágenes donde los nombres de archivo siguen un patrón específico (smoking_*.jpg y notsmoking_*.jpg):

```bash
python src/organize_images.py
```

### División del Conjunto de Datos

Para dividir el conjunto de datos en conjuntos de entrenamiento (70%), validación (15%) y prueba (15%):

```bash
python src/split_dataset.py
```

### Fuentes de Imágenes

- [Kaggle - Smoking vs Non-Smoking Dataset](https://www.kaggle.com/datasets/vitaminc/smoking-vs-non-smoking)
- [Kaggle - Smoking Detection Dataset](https://www.kaggle.com/datasets/didiruh/smoking-detection)
- Imágenes de licencia Creative Commons de Flickr, Unsplash, Pexels, etc.

## 🧠 Entrenamiento del Modelo

El modelo utiliza la arquitectura MobileNetV2 preentrenada con ImageNet para aplicar transfer learning:

```bash
python src/train_model.py
```

### Características del Entrenamiento

- **Transfer Learning**: Aprovecha conocimiento previo del modelo MobileNetV2
- **Data Augmentation**: Aumenta artificialmente el conjunto de datos mediante transformaciones
- **Optimización**: Utiliza el optimizador Adam con pérdida de entropía cruzada binaria
- **Validación**: Monitoreo continuo con conjunto de validación para evitar sobreajuste

## 📈 Evaluación y Pruebas

### Probar con Imágenes Aleatorias

Para evaluar el rendimiento del modelo con 5 imágenes aleatorias del conjunto de prueba:

```bash
python src/test_random_predictions.py
```

Este script proporciona visualizaciones con:
- Imágenes de prueba seleccionadas aleatoriamente
- Predicciones del modelo
- Etiquetas reales
- Nivel de confianza
- Indicador visual de predicciones correctas/incorrectas

## 📹 Detección en Tiempo Real

Para ejecutar la detección en tiempo real usando la webcam:

```bash
python src/webcam_detector.py
```

Esta aplicación proporciona:
- Detección en tiempo real de personas fumando
- Visualización de nivel de confianza de la predicción
- Información de FPS y tiempo de inferencia
- Interfaz visual clara con códigos de color para las predicciones

## 🥧 Implementación en Hardware Limitado

### Modelo Optimizado para Raspberry Pi y Dispositivos Similares

Para convertir el modelo a TensorFlow Lite:

```python
import tensorflow as tf

# Cargar modelo
model = tf.keras.models.load_model('models/smoking_detector_model.h5')

# Convertir a TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Guardar modelo convertido
with open('models/smoking_detector_tflite.tflite', 'wb') as f:
    f.write(tflite_model)
```

### Ejecución en Raspberry Pi

Para ejecutar el modelo optimizado en una Raspberry Pi:

```bash
python raspberry_pi/smoking_detector_rpi.py
```

### Consideraciones para Hardware Limitado

- Raspberry Pi 4/5 ofrece mejor rendimiento
- Reducir resolución de imagen mejora velocidad de inferencia
- Un acelerador como Coral USB puede mejorar significativamente el rendimiento
- Para dispositivos RISC-V como Milk-V Duo, puede ser necesaria compilación específica

## 🏆 Resultados

TODO:

## 🚀 Mejoras Futuras

- **Fine-tuning**: Descongelar capas superiores del modelo base para mayor precisión
- **Detección de Objetos**: Implementar sistema de dos etapas con YOLO para mayor precisión
- **Seguimiento Temporal**: Analizar secuencias de frames para reducir falsos positivos
- **Clasificación Multiclase**: Diferenciar entre cigarrillos convencionales y vapers
- **Optimización Avanzada**: Aplicar técnicas de cuantización y poda para mejor rendimiento

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE), lo que permite su uso, modificación y distribución libremente.

---

Desarrollado como proyecto demostrativo para integrar procesamiento de imágenes, inteligencia artificial, redes neuronales y sensores espaciales.
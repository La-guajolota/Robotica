import tensorflow as tf

# Cargar el modelo entrenado
model = tf.keras.models.load_model('models/smoking_detector_model.h5')

# Convertir a TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Guardar el modelo convertido
with open('models/smoking_detector_tflite.tflite', 'wb') as f:
    f.write(tflite_model)
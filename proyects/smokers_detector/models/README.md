# 🧠 Models

This directory contains the trained models and training history plots.

---

## 📂 Files

- **`smoking_detector_model.h5`**: The main model in HDF5 format.
- **`smoking_detector_tflite.tflite`**: The model in TensorFlow Lite format, optimized for mobile and embedded devices.
- **`plots/`**: Contains the training history plots.
  - **`training_history.png`**: A plot of the training and validation accuracy and loss.

---

## 🚀 Usage

The models in this directory can be used for inference. The `.h5` model can be loaded with TensorFlow/Keras, and the `.tflite` model can be used with the TensorFlow Lite interpreter.

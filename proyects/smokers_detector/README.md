# 🚭 Smokers Detector with AI

A real-time detection system that identifies if a person is smoking (conventional cigarette or vaper) using computer vision and deep learning.

---

## 📂 Subdirectories

- **`data/`**: Contains the raw and processed images for training and testing the model.
- **`external_references/`**: Contains external references and notebooks.
- **`models/`**: Contains the trained models and training history plots.
- **`notebooks/`**: Contains Jupyter notebooks for testing and development.
- **`src/`**: Contains the source code for the project.

---

## 🚀 Usage

This project is a real-time smoking detection system. It uses a deep learning model to detect if a person is smoking from a webcam feed.

### Requirements

To run this project, you need to have Python 3 and the required libraries installed. You can install the dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

For Raspberry Pi, use the `requirements-rapsberrypi5.txt` file:

```bash
pip install -r requirements-rapsberrypi5.txt
```

### Running the detector

To run the webcam detector, you can use the `webcam_detector.py` script:

```bash
python3 src/webcam_detector.py
```

For Raspberry Pi, use the `webcam_detector_rasp.py` script:

```bash
python3 src/webcam_detector_rasp.py
```

For more detailed instructions on how to train the model and use the other scripts, please refer to the documentation within each subdirectory.

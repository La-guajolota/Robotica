# 👁️ Vision

This directory contains scripts for testing the robot's computer vision capabilities.

---

## 📂 Files

- **`color_chnns.py`**: A script that captures video from a camera and displays the different color channels (RGB, HSV, LAB, YCrCb) and grayscale.
- **`cv.py`**: A script that processes an image to detect objects, measure their dimensions, and generate a report.
- **`height_measure.py`**: A script that captures video from a camera and detects rectangular objects, displaying their position.
- **`pixels_per_metric.py`**: A script that processes video input or a saved image to detect objects, measure their dimensions, and display the results.
- **`tests/`**: A directory containing test images and results.
- **`tests.zip`**: A zip file containing the test images and results.

---

## 🚀 Usage

To use these scripts, you need to have the required libraries installed, such as OpenCV, NumPy, and Pandas. You can install them using pip:

```bash
pip install opencv-python numpy pandas
```

You can then run the scripts from the terminal. For example, to run the `cv.py` script, you can use the following command:

```bash
python3 proyects/SCARA_robot/software/pc_tests/vision/cv.py
```

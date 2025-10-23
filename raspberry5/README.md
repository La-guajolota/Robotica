# 🍓 Raspberry Pi 5

This directory contains scripts and resources for the Raspberry Pi 5.

---

## 📂 Files

- **`servo_controller.py`**: A script for controlling servos using the `lgpio` library.
- **`mock_lgpio.py`**: A mock module for `lgpio` for development on systems without GPIO, such as a laptop.

---

## 🚀 Usage

The `servo_controller.py` script can be run on a Raspberry Pi 5 to control servos connected to its GPIO pins. The `mock_lgpio.py` module allows you to develop and test the servo controller script on a computer that does not have GPIO pins, by simulating the `lgpio` library.

### Running the servo controller

To run the servo controller on a Raspberry Pi 5, you need to have the `lgpio` library installed. You can then run the script from the terminal:

```bash
python3 servo_controller.py
```

### Using the mock library

To use the mock library for development on a non-Raspberry Pi system, you can simply run the `servo_controller.py` script. The `mock_lgpio.py` module will be automatically used instead of the real `lgpio` library.

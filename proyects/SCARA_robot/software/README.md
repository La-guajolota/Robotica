# 💻 Software

This directory contains the software for the robot, including a ROS2 workspace and firmware for an ESP32.

---

## 📂 Subdirectories

- **`esp32_microROS/`**: A PlatformIO project for the ESP32 firmware, which uses micro-ROS to communicate with the ROS2 workspace.
- **`pc_tests/`**: Contains Python scripts for testing the robot's communication and vision.
- **`rasp/`**: Contains Python scripts for the Raspberry Pi, including a GUI and a state machine.
- **`ros_scara_ws/`**: A ROS2 workspace for the robot's control and simulation.

---

## 🚀 Usage

This project is divided into several parts:

- **ESP32 Firmware**: The firmware can be compiled and uploaded to an ESP32 using PlatformIO.
- **PC Tests**: The Python scripts in this directory can be run from the terminal to test the robot's functionality.
- **Raspberry Pi**: The Python scripts in this directory are intended to be run on a Raspberry Pi.
- **ROS2 Workspace**: The ROS2 workspace can be built and run using Colcon.

For more detailed instructions, please refer to the specific documentation within each subdirectory.

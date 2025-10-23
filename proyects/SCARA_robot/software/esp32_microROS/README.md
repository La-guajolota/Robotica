# 🤖 ESP32 micro-ROS

This directory contains a PlatformIO project for the ESP32 firmware, which uses micro-ROS to communicate with the ROS2 workspace.

---

## 📂 Files

- **`platformio.ini`**: The configuration file for the PlatformIO project.
- **`src/main.cpp`**: The main source code for the firmware, which controls a SCARA robot using AS5600 encoders and Nema17 step-motors.
- **`include/` and `lib/`**: Directories for including libraries and other source files.
- **`extra_packages/`**: Contains extra packages for the project.
- **`test/`**: A directory for tests.

---

## 🚀 Usage

This firmware can be compiled and uploaded to an ESP32 using PlatformIO. To do so, you need to have PlatformIO installed.

Once installed, you can open this directory in Visual Studio Code with the PlatformIO extension and use the PlatformIO commands to build, upload, and monitor the firmware.

### Network Configuration

The firmware can be configured to use either a serial or a Wi-Fi connection to communicate with the micro-ROS agent. You can change the transport method by commenting or uncommenting the corresponding line in `src/main.cpp`:

```cpp
// #define urosAgent_serial
#define urosAgent_wifi
```

If you use the Wi-Fi transport, you need to configure your network credentials in `include/conf_network.h`.

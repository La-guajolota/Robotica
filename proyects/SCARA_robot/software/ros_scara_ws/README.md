# 🤖 ROS SCARA Workspace

This directory contains a ROS2 workspace for the robot's control and simulation.

---

## 📂 Subdirectories

- **`src/`**: Contains the source code for the ROS2 packages.
  - **`box_detector/`**: A package for detecting boxes using computer vision.
  - **`custom_msg_svrs/`**: A package that defines custom messages and services.
  - **`micro_ros_setup/`**: A package for setting up micro-ROS.
  - **`plc_chat/`**: A package for communicating with a PLC.
  - **`scara_control/`**: A package for controlling the SCARA robot.
  - **`uros/`**: Contains micro-ROS related packages.

---

## 🚀 Usage

This is a ROS2 workspace that can be built and run using Colcon.

### Build the workspace

To build the workspace, run the following command from the root of the workspace (`ros_scara_ws`):

```bash
colcon build
```

### Run the simulation

To run the simulation, you need to launch the appropriate launch file. For more information, please refer to the documentation within each package.

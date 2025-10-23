# 🚗 My Car Workspace

This directory contains a ROS2 workspace for the robot's control and simulation.

---

## 📂 Subdirectories

- **`src/`**: Contains the source code for the ROS2 packages.
  - **`my_car_description/`**: A package that contains the URDF description of the robot, as well as launch files to visualize it in RViz.

---

## 🚀 Usage

This is a ROS2 workspace that can be built and run using Colcon.

### Build the workspace

To build the workspace, run the following command from the root of the workspace (`my_car_ws`):

```bash
colcon build
```

### Run the simulation

To visualize the robot in RViz, run the following command:

```bash
ros2 launch my_car_description display.launch.xml
```

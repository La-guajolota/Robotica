import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/adrian/Desktop/ROS2_playground/SCARA_robot/software/ros_scara_ws/install/scara_control'

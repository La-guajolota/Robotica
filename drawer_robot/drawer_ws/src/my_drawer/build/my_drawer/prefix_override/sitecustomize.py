import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/media/adrian/sd_linux/sem8/Robotica/drawer_robot/drawer_ws/src/my_drawer/install/my_drawer'

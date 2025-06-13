from setuptools import find_packages
from setuptools import setup

setup(
    name='micro_ros_msgs',
    version='5.0.2',
    packages=find_packages(
        include=('micro_ros_msgs', 'micro_ros_msgs.*')),
)

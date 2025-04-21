from setuptools import find_packages
from setuptools import setup

setup(
    name='custom_msg_svrs',
    version='0.0.0',
    packages=find_packages(
        include=('custom_msg_svrs', 'custom_msg_svrs.*')),
)

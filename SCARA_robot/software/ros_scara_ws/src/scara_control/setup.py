from setuptools import find_packages, setup

package_name = 'scara_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='adrian',
    maintainer_email='adriansilpa@gmail.com',
    description='Control for Scara',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'read_encoders_node = scara_control.read_encoders_node:main',
            'move_motor_node = scara_control.move_motors_node:main'
        ],
    },
)

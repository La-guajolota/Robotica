from setuptools import find_packages, setup
"""
Esto te permitirá usar glob('meshes/*') para listar todos los archivos STL sin tener que 
enumerarlos manualmente en el futur
"""
import os
from glob import glob

package_name = 'my_drawer'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # Indicador de paquete para el ament index
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        # Instala package.xml
        ('share/' + package_name, ['package.xml']),
        # Copia todos los STL de meshes/ a share/my_drawer/meshes/
        (os.path.join('share', package_name, 'meshes'),
            glob('meshes/*')),
        # Copia todos los URDF/XACRO
        (os.path.join('share', package_name, 'urdf'),
            glob('urdf/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='adrian',
    maintainer_email='adriansilpa@gmail.com',
    description='TODO: Drawer robot controller',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'node_drawer = my_drawer.node_drawer:main'
        ],
    },
)

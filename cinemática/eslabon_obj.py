"""
Módulo para la creación y manipulación de eslabones en un sistema de coordenadas 3D.

Este módulo define la clase `Eslabon` que permite crear eslabones con ángulos de rotación y traslaciones
en un sistema de coordenadas tridimensional. También proporciona métodos para obtener la matriz homogénea
de transformación, los vectores unitarios y la posición del frame de cada eslabón.

Autor: Adrián Silva Palafox
Fecha: 11 Marzo 2025
"""
import matplotlib.pyplot as plt
import numpy as np

class Eslabon:
    def __init__(self, phi, rho, theta, x, y, z):
        self.rho = np.radians(rho)
        self.phi = np.radians(phi)
        self.theta = np.radians(theta)
        self.x = x
        self.y = y
        self.z = z
        self.matriz = self.matriz_homogenea(rho, phi, theta, x, y, z)

    def __str__(self):
        return f"Eslabon(rho={self.rho}, phi={self.phi}, theta={self.theta}, x={self.x}, y={self.y}, z={self.z})"

    @staticmethod
    def matriz_homogenea(rho=0, phi=0, theta=0, x=0, y=0, z=0):
        """
        Crea una matriz homogénea de transformación 3D.

        Parámetros:
        rho (float): Ángulo de rotación alrededor del eje Z (en radianes).
        phi (float): Ángulo de rotación alrededor del eje Y (en radianes).
        theta (float): Ángulo de rotación alrededor del eje X (en radianes).
        x (float): Traslación en el eje X.
        y (float): Traslación en el eje Y.
        z (float): Traslación en el eje Z.

        Retorna:
        numpy.ndarray: Matriz homogénea de transformación 4x4.
        """
        # Matriz de rotación y traslación
        T = np.array([
            [np.cos(rho) * np.cos(phi), np.cos(rho) * np.sin(phi) * np.sin(theta) - np.sin(rho) * np.cos(theta), np.cos(rho) * np.sin(phi) * np.cos(theta) + np.sin(rho) * np.sin(theta), x],
            [np.sin(rho) * np.cos(phi), np.sin(rho) * np.sin(phi) * np.sin(theta) + np.cos(rho) * np.cos(theta), np.sin(rho) * np.sin(phi) * np.cos(theta) - np.cos(rho) * np.sin(theta), y],
            [-np.sin(phi), np.cos(phi) * np.sin(theta), np.cos(phi) * np.cos(theta), z],
            [0, 0, 0, 1]
        ])
        return T

    def unit_vect(self):
        # Toma los vectores unitarios de las matrices homogéneas
        Xvect = self.matriz[:3, 0]
        Yvect = self.matriz[:3, 1]
        Zvect = self.matriz[:3, 2]
        return Xvect, Yvect, Zvect

    def frame_position(self):
        # Toma el vector posición
        frame_ptn = self.matriz[:3, 3]
        return frame_ptn

if "__main__" == __name__:
    j0 = Eslabon(phi=0, rho=0, theta=80, x=2, y=0, z=0) 
    j1 = Eslabon(phi=25, rho=0, theta=0, x=0, y=-1, z=0) 
    j2 = Eslabon(phi=0, rho=35, theta=0, x=0, y=0, z=2) 

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    eslabones = [j0, j1, j2]

    for eslabon in eslabones:
        # Obtiene los vectores unitarios y la posición del frame
        Xvect, Yvect, Zvect = eslabon.unit_vect()
        frame_ptn = eslabon.frame_position()
        print(f"{eslabon} - Frame position:", frame_ptn)

        # Grafica los vectores unitarios
        ax.quiver(frame_ptn[0], frame_ptn[1], frame_ptn[2], Xvect[0], Xvect[1], Xvect[2], color='r')
        ax.quiver(frame_ptn[0], frame_ptn[1], frame_ptn[2], Yvect[0], Yvect[1], Yvect[2], color='b')
        ax.quiver(frame_ptn[0], frame_ptn[1], frame_ptn[2], Zvect[0], Zvect[1], Zvect[2], color='g')

    # Configura los límites de los ejes
    ax.set_xlim([-5, 5])
    ax.set_ylim([5, -5])
    ax.set_zlim([-5, 5])

    # Etiquetas de los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Muestra la leyenda
    ax.legend()

    # Muestra la gráfica
    plt.show()
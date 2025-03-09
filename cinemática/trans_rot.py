"""
trans_rot.py

Este módulo proporciona funciones para crear y manipular matrices de rotación y traslación en 2D.
Incluye funciones para generar matrices de rotación a partir de un ángulo dado, matrices de traslación
a partir de desplazamientos en las direcciones x e y, y matrices de posición de puntos en el espacio 2D.

Autor: Adrián Silva Palafox
Fecha: 22 de febrero de 2025
"""

import numpy as np

# Matrices de rotación en theta
def rotation_matrix(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])

# Matrices de traslación en di, dj
def translation_matrix(di, dj):
    return np.array([
        [di],
        [dj]
    ])

# Matriz de la posición del punto
def origin_matirx(xi,xj):
    return np.array([
        [xi],
        [xj]
    ])

if __name__ == '__main__':
    theta = np.deg2rad(35)
    
    rotacion = rotation_matrix(theta)
    traslacion = translation_matrix(9, 10)
    punto = origin_matirx(3, 6)

    # Rotación y traslación
    rstl_matrix = np.dot(rotacion, punto) + traslacion
    print(f"Matriz de rotación:\n{rotacion}")
    print(f"Matriz de traslación:\n{traslacion}")
    print(f"Matriz de la posición del punto:\n{punto}")
    print(f"Matriz resultado:\n{rstl_matrix}")

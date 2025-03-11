"""
Autor: Adrián Silva Palafox
Fecha: Marzo 11 2025
Descripción: Este script calcula la matriz de transformación homogénea 3D para un robot con múltiples eslabones.
"""

import numpy as np

def matriz_homogenea(rho, phi, theta, x, y, z):
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

if __name__ == "__main__":
    # Solicitar el número de eslabones del robot
    J_num = int(input("¿Cuántos eslabones hay? "))
    
    # Inicializar listas para longitudes y rotaciones de los eslabones
    Ln_leght = [0] * J_num
    rho_J = [0] * J_num
    
    # Obtener longitudes y rotaciones de cada eslabón
    for Jn in range(J_num):
        Ln_leght[Jn] = float(input(f"Longitud del eslabón {Jn+1}: "))
        rho_J[Jn] = np.deg2rad(float(input(f"Rotación sobre Z del eslabón {Jn} (en grados): ")))

    # Inicializar lista para las matrices homogéneas de cada eslabón
    M_homo = [0] * J_num
    
    # Calcular la matriz homogénea para cada eslabón
    for Mn in range(J_num):
        M_homo[Mn] = matriz_homogenea(rho_J[Mn], 0, 0, Ln_leght[Mn]*np.cos(rho_J[Mn]), Ln_leght[Mn]*np.sin(rho_J[Mn]), 0)   

    # Inicializar la matriz de transformación total como una matriz identidad
    T_total = np.eye(4)

    # Multiplicar todas las matrices homogéneas para obtener la transformación total
    for Mn in range(J_num):
        T_total = np.dot(T_total, M_homo[Mn])

    # Imprimir la matriz de transformación total
    print("La matriz de transformación total es:")
    print(T_total)
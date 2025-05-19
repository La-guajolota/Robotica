"""
Calculadora de Matrices de Denavit-Hartenberg

Este script calcula las matrices de transformación utilizando el método de Denavit-Hartenberg
para análisis cinemático de robots. Permite visualizar tanto las matrices individuales
como la matriz de transformación total resultante.

Autor: Adrián Silva Palafox
Fecha: 14 de marzo de 2025
"""

import numpy as np
from numpy import pi

def DH_matrix(theta, alpha, ai, di):
    """
    Crea una matriz homogénea de transformación 3D utilizando los parámetros de Denavit-Hartenberg.
    
    Parámetros:
    -----------
    theta (float): Ángulo de rotación alrededor del eje Z (en grados).
    alpha (float): Ángulo de rotación alrededor del eje X (en grados).
    ai (float): Distancia entre los ejes Z (a lo largo del eje X).
    di (float): Distancia entre los ejes X (a lo largo del eje Z).

    Retorna:
    --------
    numpy.ndarray: Matriz homogénea de transformación 4x4 según la convención de Denavit-Hartenberg.
    """
    # Convertir de grados a radianes
    theta = np.deg2rad(theta)
    alpha = np.deg2rad(alpha)

    # Matriz de rotación y traslación
    T = np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), ai*np.cos(theta)],
        [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), ai*np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), di],
        [0, 0, 0, 1]
    ])
    
    # Redondear valores muy cercanos a cero (para evitar -0.0)
    T = np.where(np.abs(T) < 1e-10, 0, T)
    
    return T

def print_matrix(matrix, title=""):
    """
    Imprime una matriz con formato agradable en la terminal.
    
    Parámetros:
    -----------
    matrix (numpy.ndarray): Matriz a imprimir.
    title (str): Título para la matriz.
    """
    if title:
        print(f"\n{title}")
    
    # Formatear la matriz para imprimir
    for row in matrix:
        print("[", end=" ")
        for val in row:
            # Formatear números para que se vean bien
            if abs(val) < 1e-10:
                print("0.000", end=" ")
            else:
                print(f"{val:.3f}", end=" ")
        print("]")

def calcular_dh(ai, alphai, di, thetai):
    """
    Calcula todas las matrices de transformación y la matriz resultante.
    
    Parámetros:
    -----------
    ai (list): Lista de distancias a_i.
    alphai (list): Lista de ángulos alpha_i en grados.
    di (list): Lista de distancias d_i.
    thetai (list): Lista de ángulos theta_i en grados.
    
    Retorna:
    --------
    tuple: (matrices individuales, matriz resultante)
    """
    jn = len(ai)
    Tm = []  # Donde almacenamos las matrices transformación
    
    print("\n===== CÁLCULO DE MATRICES DE DENAVIT-HARTENBERG =====")
    print("Parámetros DH utilizados:")
    print(f"ai: {ai}")
    print(f"alphai: {alphai}")
    print(f"di: {di}")
    print(f"thetai: {thetai}")
    
    print("\nMatrices de transformación individuales:")
    for j in range(jn):
        T = DH_matrix(thetai[j], alphai[j], ai[j], di[j])
        Tm.append(T)
        print_matrix(T, f"Matriz T{j+1}:")
    
    # Calculamos la matriz resultante
    try:
        Trsl = np.eye(4)
        print("\nProceso de cálculo de la matriz resultante:")
        for t in range(jn):
            Trsl_prev = Trsl.copy()
            Trsl = np.dot(Trsl, Tm[t])
            print(f"\nT1_{t+1} = T1_{t} × T{t+1}:")
            print_matrix(Trsl)
            
        # Redondear valores muy pequeños a cero
        Trsl = np.where(np.abs(Trsl) < 1e-10, 0, Trsl)
        
        print("\n===== RESULTADOS FINALES =====")
        print_matrix(Trsl, "Matriz de transformación final T1_n:")
        
        # Verificación de la posición final
        pos_final = Trsl[:3, 3]
        print("\nPosición final del efector:")
        print(f"X: {pos_final[0]:.3f}")
        print(f"Y: {pos_final[1]:.3f}")
        print(f"Z: {pos_final[2]:.3f}")
        
        # Extraer matriz de rotación final
        R = Trsl[:3, :3]
        print("\nMatriz de rotación final:")
        print_matrix(R)
        
        return Tm, Trsl
        
    except np.linalg.LinAlgError as e:
        print(f"Error en la multiplicación de matrices: {e}")
        print("Puede haber indeterminaciones en la multiplicación.")
        return Tm, None

def main():
    """
    Función principal que ejecuta el programa.
    """
    print("=" * 60)
    print("CALCULADORA DE MATRICES DE DENAVIT-HARTENBERG")
    print("=" * 60)
    
    # Puedes modificar estos valores para tu caso específico
    # Datos de la tabla DH
    ai = [0, 0, 0, 175, 50, 0 ,0]
    alphai = [0, 90, 0, 0, 180, 0, 0]
    di = [113, 23, 35, 0, 0, 53, 53]
    thetai = [0, 90, 0, 0, 90, 0, 360]
    
    # Opción para ingresar datos personalizados
    opcion = input("\n¿Deseas ingresar tus propios parámetros DH? (s/n): ").lower()
    
    if opcion == 's':
        n = int(input("Ingresa el número de articulaciones: "))
        
        ai = []
        alphai = []
        di = []
        thetai = []
        
        print("\nIngresa los parámetros DH para cada articulación:")
        for i in range(n):
            print(f"\nArticulación {i+1}:")
            ai.append(float(input(f"a{i+1} (distancia entre ejes Z): ")))
            alphai.append(float(input(f"alpha{i+1} (ángulo entre ejes Z en grados): ")))
            di.append(float(input(f"d{i+1} (distancia entre ejes X): ")))
            thetai.append(float(input(f"theta{i+1} (ángulo entre ejes X en grados): ")))
    
    # Calcular matrices
    calcular_dh(ai, alphai, di, thetai)
    
    print("\n¡Cálculo completado!")
    print("=" * 60)

if __name__ == "__main__":
    main()
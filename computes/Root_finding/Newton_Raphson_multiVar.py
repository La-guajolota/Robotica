"""
Autor: Adrian Silva Palafox
Fecha: marzo 8 del 2025

Este script implementa el método de Newton-Raphson para resolver un sistema de ecuaciones no lineales.
Referencia: http://www.sc.ehu.es/sbweb/fisica3/numerico/raices/raices_5.html 

Consideraciones al usar el método de Newton-Raphson:
1. **Elección del Punto Inicial**: La elección del punto inicial es crucial para la convergencia del algoritmo.
   - **Análisis Gráfico**: Si es posible, grafica las funciones para identificar regiones donde podrían estar las raíces.
   - **Conocimiento del Problema**: Usa cualquier conocimiento previo sobre el problema para hacer una estimación inicial.
   - **Pruebas y Errores**: Prueba varios puntos iniciales diferentes para ver cuál conduce a la convergencia.
   - **Métodos Numéricos Previos**: Utiliza otros métodos numéricos más robustos para obtener una aproximación inicial.
   - **Perturbaciones Pequeñas**: Si el punto inicial está cerca de una singularidad, intenta perturbarlo ligeramente.
2. **Condición de Convergencia**: Ajusta la condición de convergencia según sea necesario. En este código, se usa `np.linalg.norm(Dx) < 1e-6`.
3. **Singularidad de la Matriz Jacobiana**: Si la matriz Jacobiana es singular, el algoritmo no podrá continuar. Se ha añadido una pequeña perturbación `epsilon` para evitar singularidades.
4. **Número de Iteraciones**: Asegúrate de que el número máximo de iteraciones `N` sea suficiente para permitir la convergencia.
5. **Interpretación de Resultados**: Verifica que los resultados sean coherentes y dentro del rango esperado. Valores extremadamente grandes o pequeños pueden indicar problemas de convergencia.
"""
#El código resuleve un problema de cinemática inversa de 2 eslabones, véase en las imagenes adjuntas a esta carpeta
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def newton_raphson_multiVar(functions, jacobian, initial_points, N=100, epsilon=1e-9):
    for initial_point in initial_points:
        print(f"\nProbando con punto inicial: {initial_point}")
        X = np.array(initial_point)  # Punto inicial
        F = lambda X: np.array([f(*X) for f in functions])  # Vector de funciones
        J = lambda X: np.array([[df(*X) for df in row] for row in jacobian])  # Matriz Jacobiana

        # Algoritmo de Newton-Raphson
        for i in range(N):
            try:
                # Calcular la inversa de la matriz Jacobiana con una pequeña perturbación
                J_inv_matrix = np.linalg.inv(J(X) + epsilon * np.eye(len(X)))
            except np.linalg.LinAlgError:
                print("La matriz Jacobiana es singular en la iteración", i)
                break
            # Calcular el cambio en X
            Dx = -np.dot(J_inv_matrix, F(X))
            # Verificar la condición de convergencia
            if np.linalg.norm(Dx) < 1e-6:
                print("Se encontró una aproximación a una raíz")
                X = X + Dx
                print(f"Iteración {i+1}: X = {X} (radianes), X = {np.degrees(X)} (grados)")
                break
            else:
                X = X + Dx
                print(f"Iteración {i+1}: X = {X} (radianes), X = {np.degrees(X)} (grados)")
        else:
            print("Se ha sobrepasado el número de iteraciones o no converge")

if __name__ == "__main__":
    # Definición del sistema de ecuaciones
    functions = [
        lambda tetha1, tetha2: 240*np.cos(tetha1) + 190*np.cos(tetha1)*np.cos(tetha2) - 190*np.sin(tetha1)*np.sin(tetha2) - 249.447,
        lambda tetha1, tetha2: 240*np.sin(tetha1) + 190*np.sin(tetha1)*np.cos(tetha2) + 190*np.cos(tetha1)*np.sin(tetha2) - 300.579
    ]

    # Derivadas parciales de cada función
    jacobian = [
        [
            lambda tetha1, tetha2: -240*np.sin(tetha1) - 190*np.sin(tetha1)*np.cos(tetha2) - 190*np.cos(tetha1)*np.sin(tetha2),
            lambda tetha1, tetha2: -190*np.cos(tetha1)*np.sin(tetha2) - 190*np.sin(tetha1)*np.cos(tetha2)
        ],
        [
            lambda tetha1, tetha2: 240*np.cos(tetha1) + 190*np.cos(tetha1)*np.cos(tetha2) - 190*np.sin(tetha1)*np.sin(tetha2),
            lambda tetha1, tetha2: -190*np.sin(tetha1)*np.sin(tetha2) + 190*np.cos(tetha1)*np.cos(tetha2)
        ]
    ]

    # Puntos iniciales para probar el método de Newton-Raphson
    initial_points = [
        [0, 0],                     # Origen
        [np.pi/4, np.pi/4],         # 45°, 45°
        [np.pi/2, np.pi/2],         # 90°, 90°
        [np.pi/6, np.pi/3],         # 30°, 60°
        [-np.pi/4, np.pi/4],        # -45°, 45°
        [np.pi/4, -np.pi/4],        # 45°, -45°
        [1.0, 0.5],                 # Aproximadamente 57° y 29°
        [0.2, 0.2],                 # Valores pequeños
        [1.5, 1.5],                 # Aproximadamente 86°
        [2.0, 0.5]                  # Aproximadamente 115° y 29°
    ]

    # Llamada a la función de Newton-Raphson
    newton_raphson_multiVar(functions, jacobian, initial_points)

    # Crear una malla de puntos para graficar las funciones
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    y = np.linspace(-2*np.pi, 2*np.pi, 100)
    X, Y = np.meshgrid(x, y)
    # Z1 = 70*np.cos(X) + 30*np.cos(X)*np.cos(Y) + 30*np.sin(X)*np.sin(Y) - 70
    # Z2 = 70*np.sin(X) + 30*np.cos(X)*np.sin(Y) + 30*np.sin(X)*np.cos(Y) - 30
    Z1 = 240*np.cos(X) + 190*np.cos(X)*np.cos(Y) - 190*np.sin(X)*np.sin(Y) - 249.447
    Z2 = 240*np.sin(X) + 190*np.sin(X)*np.cos(Y) + 190*np.cos(X)*np.sin(Y) - 300.579

    # Crear la figura 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Graficar las superficies de las funciones con colores más notables
    ax.plot_surface(X, Y, Z1, alpha=0.7, rstride=100, cstride=100, color='blue', edgecolor='none')
    ax.plot_surface(X, Y, Z2, alpha=0.7, rstride=100, cstride=100, color='red', edgecolor='none')

    # Graficar el plano Z=0
    Z0 = np.zeros_like(X)
    ax.plot_surface(X, Y, Z0, alpha=0.3, color='gray', edgecolor='none')

    # Etiquetas de los ejes
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('F(X1, X2)')

    plt.show()

    # Graficar funciones variando solo X1
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    for i, tetha2 in enumerate([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]):
        # Z1_varX1 = 70*np.cos(x) + 30*np.cos(x)*np.cos(tetha2) + 30*np.sin(x)*np.sin(tetha2) - 70
        # Z2_varX1 = 70*np.sin(x) + 30*np.cos(x)*np.sin(tetha2) + 30*np.sin(x)*np.cos(tetha2) - 30
        Z1_varX1 = 240*np.cos(x) + 190*np.cos(x)*np.cos(tetha2) - 190*np.sin(x)*np.sin(tetha2) - 249.447
        Z2_varX1 = 240*np.sin(x) + 190*np.sin(x)*np.cos(tetha2) + 190*np.cos(x)*np.sin(tetha2) - 300.579
        ax1.plot(x, Z1_varX1, label=f'tetha2={tetha2:.2f}')
        ax2.plot(x, Z2_varX1, label=f'tetha2={tetha2:.2f}')
    ax1.set_title('Variando X1')
    ax1.set_xlabel('X1')
    ax1.set_ylabel('F1(X1, tetha2)')
    ax1.legend()
    ax2.set_title('Variando X1')
    ax2.set_xlabel('X1')
    ax2.set_ylabel('F2(X1, tetha2)')
    ax2.legend()
    plt.show()

    # Graficar funciones variando solo X2
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    for i, tetha1 in enumerate([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]):
        # Z1_varX2 = 70*np.cos(tetha1) + 30*np.cos(tetha1)*np.cos(y) + 30*np.sin(tetha1)*np.sin(y) - 70
        # Z2_varX2 = 70*np.sin(tetha1) + 30*np.cos(tetha1)*np.sin(y) + 30*np.sin(tetha1)*np.cos(y) - 30
        Z1_varX2 = 240*np.cos(tetha1) + 190*np.cos(tetha1)*np.cos(y) - 190*np.sin(tetha1)*np.sin(y) - 249.447
        Z2_varX2 = 240*np.sin(tetha1) + 190*np.sin(tetha1)*np.cos(y) + 190*np.cos(tetha1)*np.sin(y) - 300.579
        ax1.plot(y, Z1_varX2, label=f'tetha1={tetha1:.2f}')
        ax2.plot(y, Z2_varX2, label=f'tetha1={tetha1:.2f}')
    ax1.set_title('Variando X2')
    ax1.set_xlabel('X2')
    ax1.set_ylabel('F1(tetha1, X2)')
    ax1.legend()
    ax2.set_title('Variando X2')
    ax2.set_xlabel('X2')
    ax2.set_ylabel('F2(tetha1, X2)')
    ax2.legend()
    plt.show()
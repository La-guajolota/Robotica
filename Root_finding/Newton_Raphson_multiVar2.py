import Newton_Raphson_multiVar as npm
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":
    # Definición del sistema de ecuaciones
    functions = [
        lambda x1, x2: x1**2 - x2**2 + 2*x2,
        lambda x1, x2: 2*x1 + x2**2 - 6,
        # Agregar más funciones si es necesario
    ]

    # Derivadas parciales de cada función
    jacobian = [
        [lambda x1, x2: 2*x1, lambda x1, x2: -2*x2 + 2],
        [lambda x1, x2: 2, lambda x1, x2: 2*x2],
        # Agregar más derivadas parciales si es necesario
    ]

    # Puntos iniciales para probar el método de Newton-Raphson
    initial_points = [
        [1.0, 1.0],
        [-1.0, 1.0],
        [-4.6, -3.8],
    ]

    # Llamada a la función de Newton-Raphson
    npm.newton_raphson_multiVar(functions, jacobian, initial_points)

    # Crear una malla de puntos para graficar las funciones
    x = np.linspace(-10, 10, 400)
    y = np.linspace(-10, 10, 400)
    X, Y = np.meshgrid(x, y)
    Z1 = X**2 - Y**2 + 2*Y
    Z2 = 2*X + Y**2 - 6

    # Crear la figura 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Graficar las superficies de las funciones
    ax.plot_surface(X, Y, Z1, alpha=0.5, rstride=100, cstride=100)
    ax.plot_surface(X, Y, Z2, alpha=0.5, rstride=100, cstride=100)

    # Etiquetas de los ejes
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('F(X1, X2)')

    plt.show()
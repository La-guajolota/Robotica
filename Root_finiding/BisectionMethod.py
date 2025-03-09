import numpy as np

def my_bisection(f, a, b, tol):
    """
    Encuentra una raíz de la función f en el intervalo [a, b] usando el método de bisección.
    Parámetros:
    f (function): La función para la cual se busca la raíz.
    a (float): El extremo inferior del intervalo.
    b (float): El extremo superior del intervalo.
    tol (float): La tolerancia para la aproximación de la raíz.
    Retorna:
    float: Una aproximación de la raíz de la función f en el intervalo [a, b].
    Lanza:
    Exception: Si no hay una raíz en el intervalo [a, b].
    """
    # Verifica si existe una raíz entre a y b
    if np.sign(f(a)) == np.sign(f(b)):
        raise Exception("Entre a y b no hay una raíz")

    m = (b + a) / 2  # punto medio en eje x en la frontera (a, b)
    
    if np.abs(f(m)) < tol:
        return m  # Es una aproximación de raíz "aceptable"
    elif np.sign(f(a)) == np.sign(f(m)):
        # CASO m -> a para optimización
        # Recursión con a = m
        return my_bisection(f, m, b, tol)
    elif np.sign(f(b)) == np.sign(f(m)):
        # CASO m -> b para optimización
        # Recursión con b = m
        return my_bisection(f, a, m, tol)

if __name__ == "__main__":
    f = lambda x: x**2 - 2

    r1 = my_bisection(f, 0, 2, 0.1)
    print(f"r1={r1}")
    
    r01 = my_bisection(f, 0, 4, 0.01)
    print(f"r01={r01}")

    # Comprobación
    print("f(r1) =", f(r1))
    print("f(r01) =", f(r01))
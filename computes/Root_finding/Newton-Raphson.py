import numpy as np

def newRaphson(f, df, x0, tol):
    """
    Calcula una estimación de la raíz de la función f utilizando el método de Newton-Raphson.

    Parámetros:
    f (function): La función de la cual se quiere encontrar la raíz.
    df (function): La derivada de la función f.
    x0 (float): El valor inicial para comenzar la iteración.
    tol (float): La tolerancia que determina la precisión de la estimación de la raíz.

    Retorna:
    float: Una estimación de la raíz de la función f.
    """
    if abs(f(x0)) < tol:
        return x0
    else:
        return newRaphson(f,df,x0-f(x0)/df(x0),tol)

if __name__ == "__main__":
    # Sin función
    f = lambda x: pow(x,2) -2 
    f_prime = lambda x: 2*x

    newton_raphson = 1.4 -f(1.4)/f_prime(1.4)

    print("Newton-Raphson", newton_raphson)
    print("sqrt(2)=",np.sqrt(2))

    #Con función
    estimate = newRaphson(f, f_prime, 1.5, 1e-6)
    print("estimate =", estimate)
    print("sqrt(2) =", np.sqrt(2))
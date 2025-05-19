import numpy as np
from scipy import optimize

# Ejemplo_0
f = lambda x: np.cos(x) - x
r = optimize.fsolve(f , -2) # Encuentra la raíces partiendo a itererar desde -2

print("r=",r)
result = f(r)
print("result=", result)

# Ejemplo_1
f1 = lambda x: 1/x # No tiene raíces
r, infodict, ier, mesg = optimize.fsolve(f1,-2,full_output=True)
print("r=",r)
result = f(r)
print("result=",result)
print(mesg) #Vemos mensaje de error
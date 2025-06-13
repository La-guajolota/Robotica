import snap7
from snap7.util import *
import time

# Crear cliente
client = snap7.client.Client()

# Conectar al PLC (IP, rack, slot)
try:
    client.connect('192.168.0.1', 0, 1)
    print("Conectado")
    # Leer datos del DB1# Leer 4 bytes desde el DB1, offset 0
    data = client.mb_read(0, 4)
    data = get_byte(data, 1)  # Obtener el primer byte
    print("Datos leídos desde el PLC:", data)

except Exception as e:
    print(f"Error al conectar al PLC: {e}")
    exit(1)
# Desconectar
client.disconnect()

print("Desconectado del PLC")

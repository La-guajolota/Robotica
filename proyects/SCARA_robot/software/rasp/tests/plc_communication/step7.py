import snap7
import struct

# Configuration
IP_PLC = "192.168.1.3"
RACK = 0
SLOT = 1

client = snap7.client.Client()

try:
    client.connect(IP_PLC, RACK, SLOT)
    print("Conectado al PLC")

    # Escribir un entero (2 bytes) a MW0 AQUI SE ESCRIBE LA ALTURA EN VALORES ENTEROS NADA DE DECIMALES
    valor_entero = 12345
    data_entero = struct.pack('>h', valor_entero)  # '>h' para short (2 bytes), big-endian
    client.mb_write(0, 2, data_entero)  # Escribir 2 bytes a partir de MW0
    print(f"Valor entero {valor_entero} escrito en MW0")

#--------------------------------------------------------------------------------------------
# Define the memory address for M8.0 TRUE O FALSE PARA SABER SI HAY CAJAS O NO
    byte_index = 8  # For M8.0, the byte index is 8
    bit_index = 0   # For M8.0, the bit index is 0

    # The boolean value you want to write (True or False)
    value_to_write = False  # Set to True for 1, or False for 0

    # Read the current byte containing M8.0 to modify only the specific bit
    # We read 1 byte starting at byte_index 8
    read_data = client.mb_read(byte_index, 1)

    # Use snap7.util.set_bool to change the specific bit in the bytearray
    snap7.util.set_bool(read_data, 0, bit_index, value_to_write)

    # Write the modified bytearray back to the PLC
    client.mb_write(byte_index, 1, read_data)
    print(f"Valor booleano '{value_to_write}' escrito en M{byte_index}.{bit_index}")


except Exception as e:
    print(f"Error: {e}")
finally:
    client.disconnect()
    print("Desconectado del PLC")

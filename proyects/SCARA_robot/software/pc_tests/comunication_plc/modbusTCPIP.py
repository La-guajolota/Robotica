import snap7
from snap7.util import *
import time

# Definir áreas manualmente
class Areas:
    MK = 0x83  # Área de memoria de marcas

# Crear cliente PLC
plc = snap7.client.Client()

def connect_to_plc(ip_address):
    """Conecta al PLC usando la dirección IP proporcionada."""
    try:
        plc.connect(ip_address, 0, 1)  # ip, rack, slot
        print(f"Conectado al PLC en {ip_address}")
    except Exception as e:
        print(f"Error al conectar al PLC: {e}")

def disconnect_from_plc():
    """Desconecta del PLC."""
    try:
        plc.disconnect()
        print("Desconectado del PLC")
    except Exception as e:
        print(f"Error al desconectar del PLC: {e}")

def read_marca(byte_index, start_byte):
    """Lee un byte de la memoria de marcas."""
    try:
        data = plc.read_area(Areas.MK, 0, byte_index, 1)
        return get_byte(data, start_byte)
    except Exception as e:
        print(f"Error al leer marcas: {e}")
        return None

def write_m_bit(byte_index, bit_index, value):
    """Escribe un bit en la memoria de marcas."""
    try:
        # Leer el byte actual de la memoria de marcas
        data = plc.read_area(Areas.MK, 0, byte_index, 1)
        # Modificar el bit específico
        set_bool(data, 0, bit_index, value)
        # Escribir el byte modificado de vuelta en la memoria de marcas
        plc.write_area(Areas.MK, 0, byte_index, data)
        print(f"Bit M{byte_index}.{bit_index} establecido en {value}")
    except Exception as e:
        print(f"Error al escribir bit: {e}")

def write_dimensions(byte_index, width, height):
    """Escribe las dimensiones de la caja (ancho y alto) en la memoria de marcas."""
    try:
        # Crear un buffer para las dimensiones
        data = bytearray(4)
        set_int(data, 0, width)  # Escribir ancho (2 bytes)
        set_int(data, 2, height)  # Escribir alto (2 bytes)
        # Escribir el buffer en la memoria de marcas
        plc.write_area(Areas.MK, 0, byte_index, data)
        print(f"Dimensiones escritas en M{byte_index}: Ancho={width}, Alto={height}")
    except Exception as e:
        print(f"Error al escribir dimensiones: {e}")

# Ejemplo funcional
if __name__ == "__main__":
    ip_address = "192.168.0.1"  # Cambiar por la IP del PLC
    connect_to_plc(ip_address)

    try:
        # Enviar información al PLC
        write_m_bit(0, 0, True)  # Hay caja (M0.0 = 1)
        write_m_bit(0, 1, False)  # Caja no forrada (M0.1 = 0)
        write_dimensions(1, 50, 30)  # Dimensiones: Ancho=50, Alto=30 (M1 y M2)

        # Leer datos de ejemplo
        print("Leyendo datos...")
        hay_caja = read_marca(0, 0)
        print(f"Hay caja: {bool(hay_caja)}")
    finally:
        disconnect_from_plc()

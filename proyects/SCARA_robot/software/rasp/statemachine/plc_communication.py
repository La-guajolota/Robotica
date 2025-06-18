# plc_communication.py
import snap7
import struct
from console_styler import styler

class PLCCommunication:
    def __init__(self, ip="192.168.1.3", rack=0, slot=1):
        self._ip = ip
        self._rack = rack
        self._slot = slot
        self._client = snap7.client.Client()
        self._connected = False

    def connect(self):
        try:
            self._client.connect(self._ip, self._rack, self._slot)
            self._connected = True
            styler.print(f"Conectado al PLC en {self._ip}", "connect", "green", bold=True)
            return True
        except Exception as e:
            styler.print(f"Error de conexión con el PLC: {e}", "error", "red")
            return False

    def disconnect(self):
        if self._connected:
            self._client.disconnect()
            self._connected = False
            styler.print("Desconectado del PLC.", "disconnect", "yellow")

    def is_connected(self):
        return self._connected

    def write_integer(self, address, value):
        try:
            data = struct.pack('>h', value)
            self._client.mb_write(address, 2, data)
            styler.print(f"Escribió el entero {value} en la dirección MW{address}", "data", "blue")
            return True
        except Exception as e:
            styler.print(f"Error escribiendo entero: {e}", "error", "red")
            return False

    def read_boolean(self, byte_index, bit_index):
        try:
            data = self._client.mb_read(byte_index, 1)
            return snap7.util.get_bool(data, 0, bit_index)
        except Exception as e:
            styler.print(f"Error leyendo booleano: {e}", "error", "red")
            return None

class PLCSimulator:
    def __init__(self):
        self._memory = {}
        self._connected = False
        styler.print("Simulador de PLC inicializado.", "plc", "cyan", bold=True)

    def connect(self):
        self._connected = True
        styler.print("Conectado al Simulador de PLC.", "connect", "green")
        return True

    def disconnect(self):
        self._connected = False
        styler.print("Desconectado del Simulador de PLC.", "disconnect", "yellow")

    def is_connected(self):
        return self._connected

    def write_integer(self, address, value):
        key = f"MW{address}"
        self._memory[key] = value
        styler.print(f"Simulador: Escribió el entero {value} en {key}", "data", "blue")
        return True

    def read_boolean(self, byte_index, bit_index):
        key = f"M{byte_index}.{bit_index}"
        return self._memory.get(key, False)

    def set_input(self, byte_index, bit_index, value):
        key = f"M{byte_index}.{bit_index}"
        self._memory[key] = value
        styler.print(f"Simulador: Entrada {key} establecida a {value}", "debug", "magenta")

    def get_memory_state(self):
        return self._memory.copy()

    def clear_memory(self):
        self._memory.clear()
        styler.print("Simulador: Memoria borrada.", "warning", "yellow")
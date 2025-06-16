import snap7
import struct

class PLCCommunication:
    def __init__(self, ip="192.168.3", rack=0, slot=1):
        self._ip = ip
        self._rack = rack
        self._slot = slot
        self._client = snap7.client.Client()

    def connect(self):
        """Connect to the PLC."""
        try:
            self._client.connect(self._ip, self._rack, self._slot)
            print("Connected to PLC")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def disconnect(self):
        """Disconnect from the PLC."""
        try:
            self._client.disconnect()
            print("Disconnected from PLC")
        except Exception as e:
            print(f"Disconnection error: {e}")

    def write_integer(self, address, value):
        """Write a 2-byte integer to the specified address."""
        try:
            data = struct.pack('>h', value)  # Pack as big-endian short (2 bytes)
            self._client.mb_write(address, 2, data)
            print(f"Integer {value} written to address {address}")
        except Exception as e:
            print(f"Error writing integer: {e}")

    def read_integer(self, address):
        """Read a 2-byte integer from the specified address."""
        try:
            data = self._client.mb_read(address, 2)
            value = struct.unpack('>h', data)[0]  # Unpack as big-endian short
            print(f"Integer read from address {address}: {value}")
            return value
        except Exception as e:
            print(f"Error reading integer: {e}")
            return None

    def write_boolean(self, byte_index, bit_index, value):
        """Write a boolean value to the specified byte and bit index."""
        try:
            data = self._client.mb_read(byte_index, 1)  # Read 1 byte
            snap7.util.set_bool(data, 0, bit_index, value)  # Modify the specific bit
            self._client.mb_write(byte_index, 1, data)  # Write back the modified byte
            print(f"Boolean '{value}' written to M{byte_index}.{bit_index}")
        except Exception as e:
            print(f"Error writing boolean: {e}")

    def read_boolean(self, byte_index, bit_index):
        """Read a boolean value from the specified byte and bit index."""
        try:
            data = self._client.mb_read(byte_index, 1)  # Read 1 byte
            value = snap7.util.get_bool(data, 0, bit_index)  # Get the specific bit
            print(f"Boolean read from M{byte_index}.{bit_index}: {value}")
            return value
        except Exception as e:
            print(f"Error reading boolean: {e}")
            return None
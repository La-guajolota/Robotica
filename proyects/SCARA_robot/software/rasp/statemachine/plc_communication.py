# plc_communication.py
import snap7
import struct
from console_styler import styler

class PLCCommunication:
    """Handles network communication with a Siemens S7 PLC using the snap7 library."""
    def __init__(self, ip="192.168.5.3", rack=0, slot=1):
        """
        Initializes the PLC client.
        
        Args:
            ip: The IP address of the PLC.
            rack: The rack number of the PLC (usually 0).
            slot: The slot number of the CPU (usually 1 or 2).
        """
        self._ip = ip
        self._rack = rack
        self._slot = slot
        self._client = snap7.client.Client()
        self._connected = False

    def connect(self):
        """Establishes a connection to the PLC."""
        try:
            self._client.connect(self._ip, self._rack, self._slot)
            self._connected = True
            styler.print(f"Connected to PLC at {self._ip}", "connect", "green", bold=True)
            return True
        except Exception as e:
            styler.print(f"PLC connection error: {e}", "error", "red")
            return False

    def disconnect(self):
        """Disconnects from the PLC."""
        if self._connected:
            self._client.disconnect()
            self._connected = False
            styler.print("Disconnected from PLC.", "disconnect", "yellow")

    def is_connected(self):
        """Returns the current connection status."""
        return self._connected

    def write_integer(self, address, value):
        """
        Writes an integer value to a Merker Word (MW) address in the PLC.
        
        Args:
            address: The starting byte address of the Merker Word (e.g., 0 for MW0).
            value: The integer value to write.
        """
        try:
            data = struct.pack('>h', value) # Pack integer into 2 bytes, big-endian
            self._client.mb_write(address, 2, data)
            styler.print(f"Wrote integer {value} to address MW{address}", "data", "blue")
            return True
        except Exception as e:
            styler.print(f"Error writing integer: {e}", "error", "red")
            return False

    def write_boolean(self, byte_index, bit_index, value_to_write):
        """
        Writes a boolean value to a specific bit of a Merker Byte (M) in the PLC.
        
        Args:
            byte_index: The address of the Merker Byte (e.g., 1 for M1).
            bit_index: The bit position within the byte (0-7).
            value_to_write: The boolean value (True or False) to write.
        """
        try:
            # Read the whole byte, modify the specific bit, then write it back
            read_data = self._client.mb_read(byte_index, 1)
            snap7.util.set_bool(read_data, 0, bit_index, value_to_write)
            self._client.mb_write(byte_index, 1, read_data)
            styler.print(f"Wrote boolean {value_to_write} to address M{byte_index}.{bit_index}", "data", "blue")
            return True
        except Exception as e:
            styler.print(f"Error writing boolean: {e}", "error", "red")
            return False

    def read_boolean(self, byte_index, bit_index):
        """
        Reads a boolean value from a specific bit of a Merker Byte (M) in the PLC.
        
        Args:
            byte_index: The address of the Merker Byte.
            bit_index: The bit position within the byte (0-7).
            
        Returns:
            The boolean value, or None if an error occurs.
        """
        try:
            data = self._client.mb_read(byte_index, 1)
            return snap7.util.get_bool(data, 0, bit_index)
        except Exception as e:
            styler.print(f"Error reading boolean: {e}", "error", "red")
            return None

class PLCSimulator:
    """
    A class that simulates a PLC for testing without a physical device.
    It uses a dictionary to mimic the PLC's memory.
    """
    def __init__(self):
        """Initializes the simulator with an empty memory."""
        self._memory = {}
        self._connected = False
        styler.print("PLC Simulator initialized.", "plc", "cyan", bold=True)

    def connect(self):
        """Simulates connecting to the PLC."""
        self._connected = True
        styler.print("Connected to PLC Simulator.", "connect", "green")
        return True

    def disconnect(self):
        """Simulates disconnecting from the PLC."""
        self._connected = False
        styler.print("Disconnected from PLC Simulator.", "disconnect", "yellow")

    def is_connected(self):
        """Returns the simulated connection status."""
        return self._connected

    def write_integer(self, address, value):
        """Simulates writing an integer to memory."""
        key = f"MW{address}"
        self._memory[key] = value
        styler.print(f"Simulator: Wrote integer {value} to {key}", "data", "blue")
        return True

    def read_boolean(self, byte_index, bit_index):
        """Simulates reading a boolean from memory. Returns False if not set."""
        key = f"M{byte_index}.{bit_index}"
        return self._memory.get(key, False)

    def set_input(self, byte_index, bit_index, value):
        """
        Allows manually setting an input bit's value in the simulator's memory.
        This is used to mimic external signals to the PLC.
        """
        key = f"M{byte_index}.{bit_index}"
        self._memory[key] = value
        styler.print(f"Simulator: Input {key} set to {value}", "debug", "magenta")

    def get_memory_state(self):
        """Returns a copy of the current simulated memory."""
        return self._memory.copy()

    def clear_memory(self):
        """Clears the simulated memory."""
        self._memory.clear()
        styler.print("Simulator: Memory cleared.", "warning", "yellow")
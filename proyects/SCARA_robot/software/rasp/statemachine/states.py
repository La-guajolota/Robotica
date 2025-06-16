from plc_communication import PLCCommunication

# Memory addresses for PLC communication
MW0 = 0  # Memory word address for integer values
M8_0 = 8  # Memory byte address for boolean values (M8.0)

class StateMachine:
    # State definitions
    IDLE = "idle"
    BOX = "box_detector"
    SCARA1 = "scara_put_box"
    SCARA2 = "scara_get_box"
    PLC_MSG = "plc_message"

    def __init__(self, plc_instance=None):
        self._state = self.IDLE  # Initial state
        self._input_register = 0b00000000  # 8-bit input register
        
        # Use provided PLC instance or create a new one
        self._plc = plc_instance if plc_instance else PLCCommunication()

    # Get the current state
    def get_state(self):
        print(f"Current state: {self._state}")
        return self._state

    # Set the current state
    def set_state(self, state):
        if state in [self.IDLE, self.BOX, self.SCARA1, self.SCARA2, self.PLC_MSG]:
            self._state = state
            print(f"State changed to: {self._state}")
        else:
            raise ValueError(f"Invalid state: {state}")

    # Get the input register value
    def get_input_register(self):
        print(f"Current input register: {bin(self._input_register)}")
        return self._input_register

    # Set the input register value
    def set_input_register(self, value):
        if isinstance(value, int) and 0 <= value <= 0xFF:  # Validate 8-bit integer
            self._input_register = value
            print(f"Input register updated to: {bin(self._input_register)}")
        else:
            raise ValueError("Input register must be an 8-bit integer.")

    # Reset the state to IDLE
    def reset_state(self):
        self._state = self.IDLE
        print("State reset to IDLE.")

    # Handle IDLE state
    def handle_idle(self):
        print("Handling IDLE state...")
        # Ejemplo: leer algún sensor del PLC
        # sensor_value = self._plc.read_boolean(0, 0)  # Lee M0.0
        self.set_state(self.BOX)

    # Handle BOX DETECTOR state
    def handle_box_detector(self):
        print("Handling BOX DETECTOR state...")
        # Ejemplo: activar detector de cajas
        # self._plc.write_boolean(1, 0, True)  # Escribe True en M1.0
        self.set_state(self.SCARA1)

    # Handle SCARA PUT BOX state
    def handle_scara_put_box(self):
        print("Handling SCARA PUT BOX state...")
        # Ejemplo: enviar comando al SCARA
        # self._plc.write_integer(100, 1)  # Escribe comando en MW100
        self.set_state(self.SCARA2)

    # Handle SCARA GET BOX state
    def handle_scara_get_box(self):
        print("Handling SCARA GET BOX state...")
        # Ejemplo: enviar otro comando al SCARA
        # self._plc.write_integer(100, 2)  # Escribe comando en MW100
        self.set_state(self.PLC_MSG)

    # Handle PLC MESSAGE state
    def handle_plc_message(self):
        print("Handling PLC MESSAGE state...")
        # Ejemplo: enviar mensaje de finalización
        # self._plc.write_boolean(2, 0, True)  # Escribe True en M2.0
        self.reset_state()
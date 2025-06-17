from plc_communication import PLCCommunication


# PLC Memory addresses
"""
MW0  full byte
MW1  next register address
-------------------------
M8.0  bit0 in M8 address
M8.1  bit1
"""
FACTOR_CONSTANT = 1
PLC_BOX_DATA = 0      # MW0 - Box height data | 2 bytes int type
PLC_REQUESTS = 8      # M8.0 - Request flags  |  

# Input register bit definitions
BIT_PLC_NEW_BOX = 0      # PLC requests new box
BIT_PLC_REMOVE_BOX = 1   # PLC requests box removal
BIT_NO_BOX_DETECTED = 2  # Webcam: no box present
BIT_PUT_ROUTINE_DONE = 3 # SCARA put routine completed
BIT_GET_ROUTINE_DONE = 4 # SCARA get routine completed
BIT_SEND_DATA = 5        # Send box data to PLC

class StateMachine:
    """State machine for box handling system coordination"""
    
    # States
    IDLE = "idle"
    BOX = "box_detector"
    SCARA1 = "scara_put_box"
    SCARA2 = "scara_get_box"
    PLC_MSG = "plc_message"

    def __init__(self, plc_instance=None):
        self._state = self.IDLE
        self._input_register = 0x00
        self._plc = plc_instance if plc_instance else PLCCommunication()


    def get_state(self):
        """Get current state"""
        return self._state

    def set_state(self, state):
        """Set new state with validation"""
        valid_states = [self.IDLE, self.BOX, self.SCARA1, self.SCARA2, self.PLC_MSG]
        if state in valid_states:
            self._state = state
            print(f"State: {state}")
        else:
            raise ValueError(f"Invalid state: {state}")

    def get_input_register(self):
        """Get input register value"""
        return self._input_register

    def _set_bit(self, bit_position):
        """Set specific bit in input register"""
        self._input_register |= (1 << bit_position)

    def _clear_register(self):
        """Clear input register"""
        self._input_register = 0x00

    def reset_state(self):
        """Reset to idle state and clear register"""
        self._clear_register()
        self._state = self.IDLE
        print("Reset to IDLE")

    def handle_idle(self):
        """Poll PLC for requests and decide next state"""
        print("IDLE: Polling PLC requests...")
        
        # Poll PLC requests
        if self._plc.read_boolean(PLC_REQUESTS, 0):
            self._set_bit(BIT_PLC_NEW_BOX)
        if self._plc.read_boolean(PLC_REQUESTS, 1):
            self._set_bit(BIT_PLC_REMOVE_BOX)

        # State transitions
        if self._input_register == 0b00000001:  # New box requested
            self.set_state(self.BOX)
        elif self._input_register == 0b00000010:  # Remove box requested
            self.set_state(self.SCARA2)
        elif self._input_register == 0b00000000:  # No requests
            self.set_state(self.IDLE)
        else:
            print(f"IDLE: Unknown register state {bin(self._input_register)}")
            self.reset_state()

    def handle_box_detector(self):
        """Check box presence with webcam"""
        print("BOX_DETECTOR: Checking box presence...")
        
        # TODO: Implement webcam/OpenCV box detection
        # box_present = detect_box()
        # if not box_present:
        #     self._set_bit(BIT_NO_BOX_DETECTED)

        # State transitions
        if self._input_register == 0b00000101:  # Need box + no box detected
            self.set_state(self.SCARA1)
        elif self._input_register == 0b00001001:  # Need box + box detected +put routine done
            self.set_state(self.PLC_MSG)
        else:
            print(f"BOX_DETECTOR: Unknown register state {bin(self._input_register)}")
            self.reset_state()

    def handle_scara_put_box(self):
        """Request SCARA robot to place box"""
        print("SCARA_PUT: Requesting box placement...")
        
        # TODO: Send ROS2 request to SCARA robot
        # success = request_scara_put_routine()
        # if success:
        #     self._set_bit(BIT_PUT_ROUTINE_DONE)

        # State transitions
        if self._input_register == 0b00001001:  # Put routine completed
            self.set_state(self.BOX)
        else:
            print(f"SCARA_PUT: Waiting for completion or retry...")

    def handle_scara_get_box(self):
        """Request SCARA robot to remove box"""
        print("SCARA_GET: Requesting box removal...")
        
        # TODO: Send ROS2 request to SCARA robot
        # success = request_scara_get_routine()
        # if success:
        #     self._set_bit(BIT_GET_ROUTINE_DONE)

        # State transitions
        if self._input_register == 0b00010010:  # Get routine completed
            self.set_state(self.IDLE)
        else:
            print(f"SCARA_GET: Waiting for completion...")

    def handle_plc_message(self):
        """Send box height data to PLC"""
        print("PLC_MSG: Sending box data...")
        
        # TODO: Get actual box height from measurement
        # box_height = measure_box_height()
        box_height = 100  # Placeholder value
        
        data = int(box_height * FACTOR_CONSTANT)
        self._plc.write_integer(PLC_BOX_DATA, data)
        print(f"Sent box height: {data}")
        
        self.reset_state()
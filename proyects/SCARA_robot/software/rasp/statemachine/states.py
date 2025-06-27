# states.py
from plc_communication import PLCCommunication
from box_detector import (
    detect_box, get_box_height, request_scara_put_routine, 
    request_scara_get_routine, is_put_routine_done, is_get_routine_done
)
from console_styler import styler

# --- Constants for PLC and State Machine Logic ---
HEIGHT_FACTOR = 1 # A factor to scale the height value before sending to the PLC.

# PLC Memory Addresses
PLC_BOX_DATA = 44      # MW0: Stores the box height data.
PLC_REQUESTS = 1      # M1.X: PLC request flags (e.g., new box, remove box).
PLC_BOX_PRESENCE = 2  # M2.X: Flags related to box presence and robot status.
PLC_MODE = 3          # M3.X: Mode flags for the PLC (e.g., manual, automatic).

# Bit positions within the internal _input_register
BIT_PLC_NEW_BOX = 0       # PLC requests a new box.
BIT_PLC_REMOVE_BOX = 1    # PLC requests to remove a box.
BIT_NO_BOX_DETECTED = 2   # Camera does not see a box.
BIT_PUT_ROUTINE_DONE = 3  # SCARA robot has finished placing a box.
BIT_GET_ROUTINE_DONE = 4  # SCARA robot has finished removing a box.
BIT_SEND_DATA = 5         # Ready to send box data to the PLC.
BIT_PLC_MODE_MANUAL = 6   # PLC is in manual/automatic mode.

class StateMachine:
    """Implements the core logic of the application by managing states and transitions."""
    
    # --- Define the possible states ---
    IDLE = "idle"
    BOX = "box_detector"
    SCARA_PUT = "scara_put_box"
    SCARA_GET = "scara_get_box"
    PLC_MSG = "plc_message"

    # --- Styling for console output for each state ---
    STATE_STYLES = {
        IDLE: {"emoji": "idle", "color": "white"},
        BOX: {"emoji": "box", "color": "yellow"},
        SCARA_PUT: {"emoji": "scara", "color": "blue"},
        SCARA_GET: {"emoji": "scara", "color": "blue"},
        PLC_MSG: {"emoji": "data", "color": "green"}
    }
    
    def __init__(self, plc_instance=None):
        """
        Initializes the state machine.
        
        Args:
            plc_instance: An instance of PLCCommunication or PLCSimulator.
        """
        self._state = self.IDLE
        self._input_register = 0x00  # A byte used to store internal flags (state inputs).
        self._plc = plc_instance if plc_instance else PLCCommunication()

    def get_state(self):
        """Returns the current state."""
        return self._state

    def set_state(self, new_state):
        """
        Changes the machine's state and prints a notification.
        
        Args:
            new_state: The state to transition to.
        """
        if new_state != self._state:
            self._state = new_state
            style = self.STATE_STYLES.get(new_state, {"emoji": "state", "color": "white"})
            styler.print(f"Transitioning to state: {new_state.upper()}", style["emoji"], style["color"], bold=True)
        else:
            style = self.STATE_STYLES.get(new_state, {"emoji": "state", "color": "white"})
            styler.print(f"Remaining in state: {new_state.upper()}", style["emoji"], style["color"])

    # --- Methods for manipulating the internal input register ---
    def _set_bit(self, bit): self._input_register |= (1 << bit)
    def _clear_bit(self, bit): self._input_register &= ~(1 << bit) 
    def _clear_register(self): self._input_register = 0x00

    # --- States ---
    def reset_state(self):
        """Resets the state machine to IDLE and clears all internal flags."""
        self._clear_register()
        styler.print("Input register cleared.", "debug")
        self.set_state(self.IDLE)
        # If using the simulator, also clear the request flags in the simulated PLC memory.
        if hasattr(self._plc, 'clear_memory'):
            self._plc.write_boolean(PLC_REQUESTS, 0, False)
            self._plc.write_boolean(PLC_REQUESTS, 1, False)

    def handle_idle(self):
        """IDLE state: Waits for a request from the PLC."""
        self.set_state(self.IDLE)
        styler.print("Polling for PLC requestsc started...", "info", "white")
        if self._plc.read_boolean(PLC_REQUESTS, 0): self._set_bit(BIT_PLC_NEW_BOX)
        if self._plc.read_boolean(PLC_REQUESTS, 1): self._set_bit(BIT_PLC_REMOVE_BOX)
        if not self._plc.read_boolean(PLC_MODE, 0): self._set_bit(BIT_PLC_MODE_MANUAL)
        styler.print("Polling for PLC requests done...", "info", "white")

        if self._input_register == 0b000001: self.set_state(self.BOX) # New box request
        elif self._input_register == 0b000010: self.set_state(self.SCARA_GET) # Remove box request
        elif self._input_register == 0b1000000:
            styler.print("PLC is in manual mode. Waiting for user input...", "manual", "cyan")
            if detect_box(): self.set_state(self.PLC_MSG) # Go to PLC_MSG state to write data to PLC.

    def handle_box_detector(self):
        """BOX state: Uses the camera to check for a box."""
        self.set_state(self.BOX)
        if not detect_box():
            styler.print("No box was detected.", "warning", "yellow")
            self._set_bit(BIT_NO_BOX_DETECTED)
            self.set_state(self.SCARA_PUT) # If no box, ask SCARA to place one.
        else:
            styler.print("Box detected. Ready to send data.", "success", "green")
            self._set_bit(BIT_SEND_DATA)
            self.set_state(self.PLC_MSG) # If box found, send its data.

    def handle_scara_put_box(self):
        """SCARA_PUT state: Manages the process of asking the SCARA robot to place a box."""
        self.set_state(self.SCARA_PUT)
        if not hasattr(self, '_put_requested'): # Send the request only once.
            styler.print("Requesting SCARA to place the box...", "scara", "blue")
            if request_scara_put_routine():
                self._put_requested = True
            else:
                styler.print("Failed to request SCARA put routine.", "error", "red")
                self.reset_state()
        
        # Once the request is sent, wait for it to be done.
        if hasattr(self, '_put_requested') and is_put_routine_done():
            styler.print("SCARA put routine completed.", "success", "green")
            self._set_bit(BIT_PUT_ROUTINE_DONE)
            delattr(self, '_put_requested') # Clear the flag for the next cycle.
            self.set_state(self.BOX) # Go back to check for the box again.
            self._clear_bit(BIT_NO_BOX_DETECTED)

    def handle_scara_get_box(self):
        """SCARA_GET state: Manages the process of asking the SCARA robot to remove a box."""
        self.set_state(self.SCARA_GET)
        if not hasattr(self, '_get_requested'): # Send the request only once.
            styler.print("Requesting SCARA to retrieve the box...", "scara", "blue")
            if request_scara_get_routine():
                self._get_requested = True
            else:
                styler.print("Failed to request SCARA get routine.", "error", "red")
        
        # Once the request is sent, wait for it to be done.
        if hasattr(self, '_get_requested') and is_get_routine_done():
            styler.print("SCARA get routine completed.", "success", "green")
            delattr(self, '_get_requested') # Clear the flag.
            self.set_state(self.PLC_MSG)

    def handle_plc_message(self):
        """PLC_MSG state: Sends the detected box's data to the PLC."""
        self.set_state(self.PLC_MSG)
        height = get_box_height()
        if height >= 5:
            # Send the box's height.
            data = int(height * HEIGHT_FACTOR)
            styler.print(f"Sending box height ({data}cm) to PLC.", "data", "green")
            self._plc.write_integer(PLC_BOX_DATA, data)

            # Let the PLC know there is a box present.
            styler.print(f"Updating M2.0 to TRUE in PLC.", "data", "green")
            self._plc.write_boolean(PLC_BOX_PRESENCE, 0, True)
        else:
            # Let the PLC know there is no box present.
            styler.print(f"Updating M2.1 to TRUE in PLC.", "data", "green")
            self._plc.write_boolean(PLC_BOX_PRESENCE, 1, True)
            styler.print("Invalid box height. Sending 0.", "warning", "yellow")
            self._plc.write_integer(PLC_BOX_DATA, 0)
        self.reset_state() # Return to IDLE after sending data.
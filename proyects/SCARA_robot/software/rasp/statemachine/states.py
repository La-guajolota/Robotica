
class state_machine:
    IDLE = "idle"
    BOX = "box_detector"
    SCARA1 = "scara_put_box"
    SCARA2 = "scara_get_box"
    PLC_MSG = "plc_message"

    def __init__(self):
        self.state = self.IDLE

    def set_state(self, state):
        if state in [self.IDLE, self.BOX, self.SCARA1, self.SCARA2, self.PLC_MSG]:
            self.state = state
        else:
            raise ValueError("Invalid state")

    def get_state(self):
        print(f"Current state: {self.state}")
        return self.state

    def is_state(self, state):
        return self.state == state

    def reset_state(self):
        self.state = None
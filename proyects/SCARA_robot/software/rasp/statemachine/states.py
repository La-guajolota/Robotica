# states.py
from plc_communication import PLCCommunication
from box_detector import (
    detect_box, get_box_height, request_scara_put_routine, 
    request_scara_get_routine, is_put_routine_done, is_get_routine_done
)
from console_styler import styler

HEIGHT_FACTOR = 1
PLC_BOX_DATA = 0
PLC_REQUESTS = 8

BIT_PLC_NEW_BOX, BIT_PLC_REMOVE_BOX = 0, 1
BIT_NO_BOX_DETECTED, BIT_PUT_ROUTINE_DONE = 2, 3
BIT_GET_ROUTINE_DONE, BIT_SEND_DATA = 4, 5

class StateMachine:
    IDLE, BOX, SCARA_PUT, SCARA_GET, PLC_MSG = "idle", "box_detector", "scara_put_box", "scara_get_box", "plc_message"

    STATE_STYLES = {
        IDLE: {"emoji": "idle", "color": "white"},
        BOX: {"emoji": "box", "color": "yellow"},
        SCARA_PUT: {"emoji": "scara", "color": "blue"},
        SCARA_GET: {"emoji": "scara", "color": "blue"},
        PLC_MSG: {"emoji": "data", "color": "green"}
    }
    
    def __init__(self, plc_instance=None):
        self._state = self.IDLE
        self._input_register = 0x00
        self._plc = plc_instance if plc_instance else PLCCommunication()

    def get_state(self):
        return self._state

    def set_state(self, new_state):
        if new_state != self._state:
            self._state = new_state
            style = self.STATE_STYLES.get(new_state, {"emoji": "state", "color": "white"})
            styler.print(f"Transición de estado a: {new_state.upper()}", style["emoji"], style["color"], bold=True)
        else:
            style = self.STATE_STYLES.get(new_state, {"emoji": "state", "color": "white"})
            styler.print(f"Permaneciendo en estado: {new_state.upper()}", style["emoji"], style["color"])


    def _set_bit(self, bit): self._input_register |= (1 << bit)
    def _clear_bit(self, bit): self._input_register &= ~(1 << bit) 
    def _clear_register(self): self._input_register = 0x00

    def reset_state(self):
        self._clear_register()
        styler.print("Registro de entrada limpiado.", "debug")
        self.set_state(self.IDLE)
        # Limpiar banderas de solicitud en el PLC simulado si aplica
        if hasattr(self._plc, 'clear_memory'):
            self._plc.write_boolean(PLC_REQUESTS, 0, False)
            self._plc.write_boolean(PLC_REQUESTS, 1, False)

    def handle_idle(self):
        self.set_state(self.IDLE)
        styler.print("Sondeando solicitudes del PLC...", "info", "white")
        if self._plc.read_boolean(PLC_REQUESTS, 0): self._set_bit(BIT_PLC_NEW_BOX)
        if self._plc.read_boolean(PLC_REQUESTS, 1): self._set_bit(BIT_PLC_REMOVE_BOX)

        if self._input_register == 0b000001: self.set_state(self.BOX)
        elif self._input_register == 0b000010: self.set_state(self.SCARA_GET)

    def handle_box_detector(self):
        self.set_state(self.BOX)
        if not detect_box():
            styler.print("No se detectó ninguna caja.", "warning", "yellow")
            self._set_bit(BIT_NO_BOX_DETECTED)
            self.set_state(self.SCARA_PUT)
        else:
            styler.print("Caja detectada. Listo para enviar datos.", "success", "green")
            self._set_bit(BIT_SEND_DATA)
            self.set_state(self.PLC_MSG)

    def handle_scara_put_box(self):
        self.set_state(self.SCARA_PUT)
        if not hasattr(self, '_put_requested'):
            styler.print("Solicitando al SCARA que coloque la caja...", "scara", "blue")
            if request_scara_put_routine():
                self._put_requested = True
            else:
                styler.print("Fallo al solicitar la rutina de colocación de SCARA.", "error", "red")
                self.reset_state()
        
        if hasattr(self, '_put_requested') and is_put_routine_done():
            styler.print("Rutina de colocación de SCARA completada.", "success", "green")
            self._set_bit(BIT_PUT_ROUTINE_DONE)
            delattr(self, '_put_requested')
            self.set_state(self.BOX) # Volver a verificar la caja
            self._clear_bit(BIT_NO_BOX_DETECTED)

    def handle_scara_get_box(self):
        self.set_state(self.SCARA_GET)
        if not hasattr(self, '_get_requested'):
            styler.print("Solicitando al SCARA que retire la caja...", "scara", "blue")
            if request_scara_get_routine():
                self._get_requested = True
            else:
                styler.print("Fallo al solicitar la rutina de retirada de SCARA.", "error", "red")
        
        if hasattr(self, '_get_requested') and is_get_routine_done():
            styler.print("Rutina de retirada de SCARA completada.", "success", "green")
            delattr(self, '_get_requested')
            self.reset_state()

    def handle_plc_message(self):
        self.set_state(self.PLC_MSG)
        height = get_box_height()
        if height > 0:
            data = int(height * HEIGHT_FACTOR)
            styler.print(f"Enviando altura de la caja ({data}px) al PLC.", "data", "green")
            self._plc.write_integer(PLC_BOX_DATA, data)
        else:
            styler.print("Altura de caja no válida. Enviando 0.", "warning", "yellow")
            self._plc.write_integer(PLC_BOX_DATA, 0)
        self.reset_state()
# mock_lgpio.py - Módulo mock de lgpio para desarrollo en laptop

import time
import platform
from typing import Optional, Dict, Any

class LGPIOError(Exception):
    """Excepción personalizada que imita lgpio.error"""
    pass

class MockLGPIO:
    """Mock de lgpio para desarrollo en sistemas sin GPIO"""
    
    def __init__(self):
        self.chips: Dict[int, bool] = {}
        self.pwm_channels: Dict[tuple, Dict[str, Any]] = {}  # (chip, pin) -> config
        self.pin_states: Dict[tuple, int] = {}  # (chip, pin) -> state
        self.debug = True
        
    def gpiochip_open(self, device: int) -> int:
        """Mock de gpiochip_open"""
        if self.debug:
            print(f"[MOCK] Opening GPIO chip {device}")
        
        if device in self.chips:
            raise LGPIOError(f"chip {device} already open")
            
        self.chips[device] = True
        return device
    
    def gpiochip_close(self, handle: int) -> None:
        """Mock de gpiochip_close"""
        if self.debug:
            print(f"[MOCK] Closing GPIO chip {handle}")
            
        if handle not in self.chips:
            raise LGPIOError(f"chip {handle} not open")
            
        # Limpiar PWM channels de este chip
        keys_to_remove = [key for key in self.pwm_channels.keys() if key[0] == handle]
        for key in keys_to_remove:
            del self.pwm_channels[key]
            
        del self.chips[handle]
    
    def tx_pwm(self, handle: int, pin: int, frequency: float, duty_cycle: float) -> None:
        """Mock de tx_pwm"""
        if handle not in self.chips:
            raise LGPIOError(f"chip {handle} not open")
            
        key = (handle, pin)
        
        if duty_cycle == 0 and frequency == 0:
            # Detener PWM
            if key in self.pwm_channels:
                del self.pwm_channels[key]
                if self.debug:
                    print(f"[MOCK] PWM stopped on chip {handle}, pin {pin}")
        else:
            # Configurar PWM
            self.pwm_channels[key] = {
                'frequency': frequency,
                'duty_cycle': duty_cycle,
                'active': True
            }
            if self.debug:
                print(f"[MOCK] PWM configured: chip {handle}, pin {pin}, "
                      f"freq {frequency}Hz, duty {duty_cycle:.2f}%")
    
    def gpio_read(self, handle: int, pin: int) -> int:
        """Mock de gpio_read"""
        if handle not in self.chips:
            raise LGPIOError(f"chip {handle} not open")
            
        key = (handle, pin)
        state = self.pin_states.get(key, 0)
        
        if self.debug:
            print(f"[MOCK] Reading pin {pin}: {state}")
            
        return state
    
    def gpio_write(self, handle: int, pin: int, level: int) -> None:
        """Mock de gpio_write"""
        if handle not in self.chips:
            raise LGPIOError(f"chip {handle} not open")
            
        key = (handle, pin)
        self.pin_states[key] = level
        
        if self.debug:
            print(f"[MOCK] Writing pin {pin}: {level}")
    
    def gpio_claim_output(self, handle: int, pin: int, level: int = 0) -> None:
        """Mock de gpio_claim_output"""
        if handle not in self.chips:
            raise LGPIOError(f"chip {handle} not open")
            
        key = (handle, pin)
        self.pin_states[key] = level
        
        if self.debug:
            print(f"[MOCK] Claimed pin {pin} as output, initial level: {level}")
    
    def gpio_claim_input(self, handle: int, pin: int) -> None:
        """Mock de gpio_claim_input"""
        if handle not in self.chips:
            raise LGPIOError(f"chip {handle} not open")
            
        if self.debug:
            print(f"[MOCK] Claimed pin {pin} as input")
    
    def gpio_free(self, handle: int, pin: int) -> None:
        """Mock de gpio_free"""
        if handle not in self.chips:
            raise LGPIOError(f"chip {handle} not open")
            
        key = (handle, pin)
        if key in self.pin_states:
            del self.pin_states[key]
            
        if self.debug:
            print(f"[MOCK] Freed pin {pin}")
    
    def set_debug(self, enabled: bool) -> None:
        """Habilitar/deshabilitar debug prints"""
        self.debug = enabled
        print(f"[MOCK] Debug {'enabled' if enabled else 'disabled'}")
    
    def get_pwm_status(self) -> Dict:
        """Método adicional para debugging - ver estado de PWM"""
        return dict(self.pwm_channels)
    
    def simulate_servo_feedback(self, handle: int, pin: int) -> Optional[float]:
        """Simular feedback de un servo basado en la configuración PWM"""
        key = (handle, pin)
        if key not in self.pwm_channels:
            return None
            
        config = self.pwm_channels[key]
        duty = config['duty_cycle']
        
        # Convertir duty cycle a ángulo aproximado para servo SG90
        # Asumiendo 1ms-2ms pulsos en período de 20ms (50Hz)
        if config['frequency'] == 50:  # Servo frequency
            pulse_width_ms = (duty / 100) * 20  # duty cycle a ms en período 20ms
            if 1 <= pulse_width_ms <= 2:
                angle = (pulse_width_ms - 1) * 180  # 1ms=0°, 2ms=180°
                return angle
        
        return None

# Auto-detección del sistema
def get_lgpio():
    """
    Retorna el módulo lgpio real en Raspberry Pi, 
    o el mock en otros sistemas
    """
    system_info = platform.machine().lower()
    is_raspberry_pi = any(arch in system_info for arch in ['arm', 'aarch64'])
    
    if is_raspberry_pi:
        try:
            import lgpio
            print("[INFO] Using real lgpio on Raspberry Pi")
            return lgpio
        except ImportError:
            print("[WARNING] lgpio not installed, using mock")
            mock = MockLGPIO()
            mock.error = LGPIOError
            return mock
    else:
        print("[INFO] Using mock lgpio for development")
        mock = MockLGPIO()
        mock.error = LGPIOError
        return mock

# Para uso directo
lgpio = get_lgpio()
error = LGPIOError
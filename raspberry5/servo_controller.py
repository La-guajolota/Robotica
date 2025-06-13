# servo_controller.py - Ejemplo de uso del mock lgpio

import time
import sys
from pathlib import Path

# Importar nuestro mock lgpio
try:
    from mock_lgpio import lgpio
except ImportError:
    # Si estás en la Pi, usar lgpio real
    import lgpio

class ServoController:
    """Controlador de servos que funciona tanto en desarrollo como en Pi"""
    
    def __init__(self, pins: list, wait: float = 0.01):
        """
        Inicializar controlador de servos
        
        Args:
            pins: Lista de pines GPIO para los servos
            wait: Factor de espera entre comandos
        """
        self.pins = pins
        self.wait = wait
        self.chip = None
        self.virtual = False
        
        try:
            # Intentar inicializar GPIO
            self.chip = lgpio.gpiochip_open(0)
            
            # Configurar PWM a 50Hz para todos los pines
            for pin in self.pins:
                lgpio.tx_pwm(self.chip, pin, 50, 0)  # 50Hz, 0% duty inicial
                
            self.virtual = False
            print(f"[INFO] Servo controller initialized for pins: {self.pins}")
            
        except (AttributeError, lgpio.error) as e:
            print(f"[ERROR] GPIO not available: {e}")
            self.virtualise()
    
    def virtualise(self):
        """Activar modo virtual cuando no hay GPIO disponible"""
        self.virtual = True
        self.chip = None
        print("[INFO] Running in virtual mode - no actual servo control")
    
    def set_servo_angle(self, pin: int, angle: float):
        """
        Mover servo a ángulo específico
        
        Args:
            pin: Pin GPIO del servo
            angle: Ángulo en grados (0-180)
        """
        if self.virtual:
            print(f"[VIRTUAL] Servo on pin {pin} -> {angle}°")
            return
        
        if pin not in self.pins:
            raise ValueError(f"Pin {pin} not configured for servo control")
        
        # Limitar ángulo
        angle = max(0, min(180, angle))
        
        # SG90: 1ms = 0°, 1.5ms = 90°, 2ms = 180°
        pulse_width_ms = 1.0 + (angle / 180.0)  # 1-2ms
        
        # Convertir a duty cycle para 50Hz (período 20ms)
        duty_cycle = (pulse_width_ms / 20.0) * 100
        
        try:
            lgpio.tx_pwm(self.chip, pin, 50, duty_cycle)
            print(f"[SERVO] Pin {pin} -> {angle}° (duty: {duty_cycle:.2f}%)")
            
            # Feedback simulado si es mock
            if hasattr(lgpio, 'simulate_servo_feedback'):
                feedback_angle = lgpio.simulate_servo_feedback(self.chip, pin)
                if feedback_angle is not None:
                    print(f"[FEEDBACK] Simulated angle: {feedback_angle:.1f}°")
                    
        except lgpio.error as e:
            print(f"[ERROR] Failed to control servo on pin {pin}: {e}")
        
        time.sleep(self.wait)
    
    def set_servo_pulsewidth(self, pin: int, pulsewidth: int):
        """
        Control directo por ancho de pulso (compatibilidad con pigpio)
        
        Args:
            pin: Pin GPIO del servo  
            pulsewidth: Ancho de pulso en microsegundos (1000-2000)
        """
        if pulsewidth == 0:
            self.stop_servo(pin)
            return
        
        # Convertir microsegundos a ángulo
        pulsewidth_ms = pulsewidth / 1000.0
        if pulsewidth_ms < 1.0 or pulsewidth_ms > 2.0:
            print(f"[WARNING] Pulsewidth {pulsewidth}μs out of safe range")
        
        angle = (pulsewidth_ms - 1.0) * 180
        self.set_servo_angle(pin, angle)
    
    def stop_servo(self, pin: int):
        """Detener PWM en un pin específico"""
        if self.virtual:
            print(f"[VIRTUAL] Stopping servo on pin {pin}")
            return
        
        try:
            lgpio.tx_pwm(self.chip, pin, 0, 0)  # Detener PWM
            print(f"[SERVO] Stopped servo on pin {pin}")
        except lgpio.error as e:
            print(f"[ERROR] Failed to stop servo on pin {pin}: {e}")
    
    def sweep_servo(self, pin: int, start_angle: float = 0, 
                   end_angle: float = 180, steps: int = 10, delay: float = 0.5):
        """
        Hacer un barrido suave del servo
        
        Args:
            pin: Pin del servo
            start_angle: Ángulo inicial
            end_angle: Ángulo final  
            steps: Número de pasos
            delay: Tiempo entre pasos
        """
        print(f"[SWEEP] Pin {pin}: {start_angle}° -> {end_angle}° in {steps} steps")
        
        for i in range(steps + 1):
            angle = start_angle + (end_angle - start_angle) * (i / steps)
            self.set_servo_angle(pin, angle)
            time.sleep(delay)
    
    def cleanup(self):
        """Limpiar recursos GPIO"""
        if self.virtual:
            print("[CLEANUP] Virtual mode - nothing to cleanup")
            return
        
        try:
            # Detener PWM en todos los pines
            for pin in self.pins:
                lgpio.tx_pwm(self.chip, pin, 0, 0)
            
            # Cerrar chip
            if self.chip is not None:
                lgpio.gpiochip_close(self.chip)
                
            print("[CLEANUP] GPIO resources cleaned up")
            
        except lgpio.error as e:
            print(f"[ERROR] Cleanup failed: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()

# Ejemplo de uso
def main():
    """Función principal de demostración"""
    # Configurar servos en pines 14 y 15 (como tu código original)
    servo_pins = [14, 15]
    
    # Habilitar debug si es mock
    if hasattr(lgpio, 'set_debug'):
        lgpio.set_debug(True)
    
    # Usar context manager para cleanup automático
    with ServoController(servo_pins, wait=0.01) as controller:
        
        print("\n=== Demo de Control de Servos ===")
        
        # Test 1: Ángulos específicos
        print("\n1. Movimiento a ángulos específicos:")
        angles = [0, 45, 90, 135, 180]
        for angle in angles:
            controller.set_servo_angle(14, angle)
            controller.set_servo_angle(15, 180 - angle)  # Espejo
            time.sleep(1)
        
        # Test 2: Control por pulsewidth (compatibilidad pigpio)
        print("\n2. Control por ancho de pulso:")
        pulsewidths = [1000, 1250, 1500, 1750, 2000]  # μs
        for pw in pulsewidths:
            controller.set_servo_pulsewidth(14, pw)
            time.sleep(0.8)
        
        # Test 3: Barrido suave
        print("\n3. Barrido suave:")
        controller.sweep_servo(14, 0, 180, steps=20, delay=0.1)
        controller.sweep_servo(15, 180, 0, steps=20, delay=0.1)
        
        # Test 4: Detener servos
        print("\n4. Deteniendo servos:")
        controller.stop_servo(14)
        controller.stop_servo(15)
        
        print("\n=== Demo completada ===")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
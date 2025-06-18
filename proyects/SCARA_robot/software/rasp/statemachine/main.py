# main.py
import signal
import sys
import threading
from time import sleep
from states import StateMachine
from plc_communication import PLCCommunication, PLCSimulator
from box_detector import initialize_box_detector, cleanup_box_detector
from console_styler import styler

LOOP_DELAY = 3

def signal_handler(sig, frame):
    styler.print("\n¡Apagando el sistema de forma ordenada!", "bye", "yellow", bold=True)
    cleanup_box_detector()
    sys.exit(0)

def user_input_thread(plc_sim):
    styler.print_title("Panel de Control del Simulador de PLC", color="blue")
    print("  Comandos:")
    styler.print("new    - Solicitar nueva caja (M8.0 = True)", "prompt", "white")
    styler.print("remove - Solicitar retirada de caja (M8.1 = True)", "prompt", "white")
    styler.print("clear  - Limpiar todas las entradas del PLC", "prompt", "white")
    styler.print("status - Mostrar el estado de la memoria del PLC", "prompt", "white")
    styler.print("quit   - Salir del programa", "prompt", "white")
    styler.print_separator()
    
    while True:
        try:
            cmd = styler.get_input("Comando PLC").strip().lower()
            if cmd == "new":
                plc_sim.set_input(8, 0, True)
            elif cmd == "remove":
                plc_sim.set_input(8, 1, True)
            elif cmd == "clear":
                plc_sim.clear_memory()
            elif cmd == "status":
                memory = plc_sim.get_memory_state()
                styler.print("Estado de la Memoria del PLC:", "debug", "cyan", bold=True)
                if not memory:
                    styler.print("  (Memoria vacía)", "info", "white")
                for key, value in memory.items():
                    styler.print(f"  {key}: {value}", "info", "white")
            elif cmd == "quit":
                signal_handler(None, None)
        except (EOFError, KeyboardInterrupt):
            signal_handler(None, None)
            break

def main():
    styler.print_title("Sistema de Manipulación de Cajas")
    signal.signal(signal.SIGINT, signal_handler)
    
    styler.print("Seleccione el modo de operación:", "system", "cyan", bold=True)
    print("1. Modo PLC Real")
    print("2. Modo Simulación")
    
    choice = ""
    while choice not in ['1', '2']:
        choice = styler.get_input("Ingrese su elección (1 o 2)")

    if choice == '1':
        styler.print("\nModo PLC Real - Conectando...", "plc", "yellow")
        plc_ip = styler.get_input("IP del PLC (default: 192.168.1.3)") or "192.168.1.3"
        plc = PLCCommunication(ip=plc_ip)
        if not plc.connect(): return
    else:
        styler.print("\nModo Simulación - Iniciando...", "plc", "yellow")
        plc = PLCSimulator()
        plc.connect()
        threading.Thread(target=user_input_thread, args=(plc,), daemon=True).start()
    
    initialize_box_detector()
    state_machine = StateMachine(plc_instance=plc)
    
    styler.print("¡Sistema inicializado con éxito!", "success", "green", bold=True)
    styler.print("La máquina de estados está comenzando...", "loop", "cyan")
    styler.print_separator()

    try:
        while True:
            current_state = state_machine.get_state()
            
            # Ejecución de la máquina de estados
            if current_state == state_machine.IDLE: state_machine.handle_idle()
            elif current_state == state_machine.BOX: state_machine.handle_box_detector()
            elif current_state == state_machine.SCARA_PUT: state_machine.handle_scara_put_box()
            elif current_state == state_machine.SCARA_GET: state_machine.handle_scara_get_box()
            elif current_state == state_machine.PLC_MSG: state_machine.handle_plc_message()
            
            sleep(LOOP_DELAY)
            styler.print_separator()
            
    except Exception as e:
        styler.print(f"Error inesperado: {e}", "error", "red", bold=True)
    finally:
        styler.print("Limpiando recursos...", "system", "yellow")
        cleanup_box_detector()
        if plc: plc.disconnect()
        styler.print("Apagado del sistema completo.", "bye", "green", bold=True)

if __name__ == "__main__":
    main()
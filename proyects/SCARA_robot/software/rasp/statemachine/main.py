# main.py
import signal
import sys
import threading
from time import sleep
from states import StateMachine
from plc_communication import PLCCommunication, PLCSimulator
from box_detector import initialize_box_detector, cleanup_box_detector
from console_styler import styler

# Delay in seconds for the main application loop.
LOOP_DELAY = 3

def signal_handler(sig, frame):
    """Handles the shutdown signal (Ctrl+C) to exit gracefully."""
    styler.print("\nShutting down the system gracefully!", "bye", "yellow", bold=True)
    cleanup_box_detector()  # Ensure camera resources are released.
    sys.exit(0)

def user_input_thread(plc_sim):
    """
    Runs in a separate thread to handle user commands for the PLC simulator.
    
    Args:
        plc_sim: The PLCSimulator instance.
    """
    styler.print_title("PLC Simulator Control Panel", color="blue")
    print("  Commands:")
    styler.print("new    - Request new box (M8.0 = True)", "prompt", "white")
    styler.print("remove - Request box removal (M8.1 = True)", "prompt", "white")
    styler.print("clear  - Clear all PLC inputs", "prompt", "white")
    styler.print("status - Show PLC memory state", "prompt", "white")
    styler.print("quit   - Exit the program", "prompt", "white")
    styler.print_separator()
    
    while True:
        try:
            cmd = styler.get_input("PLC Command").strip().lower()
            if cmd == "new":
                plc_sim.set_input(8, 0, True) # Simulate PLC request for a new box.
            elif cmd == "remove":
                plc_sim.set_input(8, 1, True) # Simulate PLC request to remove a box.
            elif cmd == "clear":
                plc_sim.clear_memory()
            elif cmd == "status":
                memory = plc_sim.get_memory_state()
                styler.print("PLC Memory State:", "debug", "cyan", bold=True)
                if not memory:
                    styler.print("  (Memory is empty)", "info", "white")
                for key, value in memory.items():
                    styler.print(f"  {key}: {value}", "info", "white")
            elif cmd == "quit":
                signal_handler(None, None)
        except (EOFError, KeyboardInterrupt):
            signal_handler(None, None)
            break

def main():
    """The main entry point for the application."""
    styler.print_title("Box Manipulation System")
    signal.signal(signal.SIGINT, signal_handler) # Register the shutdown handler.
    
    # Let the user choose between a real PLC and a simulator.
    styler.print("Select operation mode:", "system", "cyan", bold=True)
    print("1. Real PLC Mode")
    print("2. Simulation Mode")
    
    choice = ""
    while choice not in ['1', '2']:
        choice = styler.get_input("Enter your choice (1 or 2)")

    if choice == '1':
        styler.print("\nReal PLC Mode - Connecting...", "plc", "yellow")
        plc_ip = styler.get_input("PLC IP (default: 192.168.1.3)") or "192.168.1.3"
        plc = PLCCommunication(ip=plc_ip)
        if not plc.connect(): return # Exit if connection fails.
    else:
        styler.print("\nSimulation Mode - Starting...", "plc", "yellow")
        plc = PLCSimulator()
        plc.connect()
        # Start the user input thread for the simulator
        threading.Thread(target=user_input_thread, args=(plc,), daemon=True).start()
    
    # Initialize the system components
    initialize_box_detector()
    state_machine = StateMachine(plc_instance=plc)
    
    styler.print("System initialized successfully!", "success", "green", bold=True)
    styler.print("State machine is starting...", "loop", "cyan")
    styler.print_separator()

    try:
        # Main application loop
        while True:
            current_state = state_machine.get_state()
            styler.print(f"Input_registers: {bin(state_machine._input_register)}", "info", "white")
            
            # Execute the logic for the current state
            if current_state == state_machine.IDLE: state_machine.handle_idle()
            elif current_state == state_machine.BOX: state_machine.handle_box_detector()
            elif current_state == state_machine.SCARA_PUT: state_machine.handle_scara_put_box()
            elif current_state == state_machine.SCARA_GET: state_machine.handle_scara_get_box()
            elif current_state == state_machine.PLC_MSG: state_machine.handle_plc_message()
            
            sleep(LOOP_DELAY)
            styler.print_separator()

            
    except Exception as e:
        styler.print(f"Unexpected error: {e}", "error", "red", bold=True)
    finally:
        # Cleanup resources before exiting
        styler.print("Cleaning up resources...", "system", "yellow")
        cleanup_box_detector()
        if plc: plc.disconnect()
        styler.print("System shutdown complete.", "bye", "green", bold=True)

if __name__ == "__main__":
    main()      
from time import sleep
from states import StateMachine
from plc_communication import PLCCommunication

def main():
    # Crear la instancia del PLC una sola vez
    plc = PLCCommunication(ip="192.168.1.3")  # Ajusta la IP según tu configuración
    
    # Conectar al PLC
    if not plc.connect():
        print("Failed to connect to PLC. Exiting...")
        # return
    
    # Crear la máquina de estados pasándole la instancia del PLC
    st_machine = StateMachine(plc_instance=plc)

    try:
        while True:
            match st_machine.get_state():
                case st_machine.IDLE:
                    st_machine.handle_idle()
                case st_machine.BOX:
                    st_machine.handle_box_detector()
                case st_machine.SCARA1:
                    st_machine.handle_scara_put_box()
                case st_machine.SCARA2:
                    st_machine.handle_scara_get_box()
                case st_machine.PLC_MSG:
                    st_machine.handle_plc_message()
            sleep(1)
            
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    finally:
        # Desconectar del PLC al salir
        plc.disconnect()

if __name__ == "__main__":
    main()
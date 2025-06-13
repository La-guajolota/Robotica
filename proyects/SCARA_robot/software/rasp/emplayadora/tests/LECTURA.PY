import snap7
from snap7.util import get_int, get_byte

def leer_memoria_plc():
    """Función simple para leer memoria del PLC"""
    
    # Configuración del PLC
    PLC_IP = "192.168.1.1"  # Cambia por la IP de tu PLC
    RACK = 0
    SLOT = 1
    
    # Crear cliente Snap7
    client = snap7.client.Client()
    
    try:
        # Conectar al PLC
        print(f"Conectando al PLC en {PLC_IP}...")
        client.connect(PLC_IP, RACK, SLOT)
        print("✅ Conectado exitosamente!")
        
        # Leer memoria M (Merker) - 4 bytes desde M0
        print("\n📖 Leyendo memoria...")
        data = client.mb_read(0, 4)  # Leer 4 bytes desde M0
        
        # Extraer valores
        valor_M0 = get_byte(data, 0)    # Byte en M0
        valor_M1 = get_byte(data, 1)    # Byte en M1
        valor_M0_M1 = get_int(data, 0)  # Entero de 16 bits desde M0
        
        # Mostrar resultados
        print("📊 Valores leídos:")
        print(f"   M0 (byte): {valor_M0}")
        print(f"   M1 (byte): {valor_M1}")
        print(f"   M0-M1 (int): {valor_M0_M1}")
        
    except Exception as e:
        print(f" Error: {e}")
        
    finally:
        # Desconectar
        client.disconnect()
        print("Desconectado del PLC")

if __name__ == "__main__":
    leer_memoria_plc()
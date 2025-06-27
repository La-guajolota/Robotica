# plc_connector.py
import snap7
from snap7.util import *
import threading
import time
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from config import get_firebase_config, DATABASE_CONFIG
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PLCConnector:
    def __init__(self, plc_ip="192.168.5.3", rack=0, slot=1):
        """
        Inicializa el conector PLC
        
        Args:
            plc_ip (str): IP del PLC
            rack (int): Número de rack del PLC
            slot (int): Número de slot del PLC
        """
        self.plc_ip = plc_ip
        self.rack = rack
        self.slot = slot
        self.client = snap7.client.Client()
        self.running = False
        self.db = None
        
        # Configuración de tags del PLC usando memoria M (Merker)
        # Variables TIME ajustadas para ocupar 4 bytes cada una
        self.tags_config = {
            "box_count": {"area": "M", "start": 8, "size": 2, "type": "int"},
            "machine_speed": {"area": "M", "start": 2, "size": 2, "type": "int"},
            "system_status": {"area": "M", "start": 3, "size": 1, "type": "bool"},
            "production_time": {"area": "M", "start": 40, "size": 4, "type": "time"},  # Cambiado a TIME
            "remaining_cycles": {"area": "M", "start": 16, "size": 2, "type": "int"},
            "cycles": {"area": "M", "start": 6, "size": 2, "type": "int"},
            "active_time": {"area": "M", "start": 10, "size": 4, "type": "time"},     # Cambiado a TIME
            "stop_time": {"area": "M", "start": 24, "size": 4, "type": "time"}       # Cambiado a TIME
        }
        
        # Diccionario de códigos de error
        self.error_codes = {
            0: "OK",
            373: "Error código 373: Falla de sensor",
            100: "Error de comunicación",
            200: "Falla mecánica",
            300: "Error de temperatura",
            # Agregar más códigos según necesites
        }
        
        self.init_firebase()
    
    def format_time(self, ms):
        """Convierte milisegundos a formato legible"""
        if ms < 1000:
            return f"{ms} ms"
        elif ms < 60000:
            return f"{ms/1000:.1f} s"
        elif ms < 3600000:
            return f"{ms/60000:.1f} min"
        else:
            return f"{ms/3600000:.1f} h"
    
    def init_firebase(self):
        """Inicializa la conexión con Firebase"""
        try:
            cred = get_firebase_config()
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            logger.info("Firebase inicializado correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar Firebase: {e}")
    
    def connect_plc(self):
        """Conecta al PLC"""
        try:
            logger.info(f"Intentando conectar con PLC en {self.plc_ip}:{self.rack}.{self.slot}")
            self.client.connect(self.plc_ip, self.rack, self.slot)
            logger.info(f"Conectado al PLC en {self.plc_ip}")
            return True
        except Exception as e:
            logger.error(f"Error al conectar con PLC: {e}")
            return False
    
    def disconnect_plc(self):
        """Desconecta del PLC"""
        try:
            self.client.disconnect()
            logger.info("Desconectado del PLC")
        except Exception as e:
            logger.error(f"Error al desconectar: {e}")
    
    def read_tag(self, tag_name):
        """
        Lee un tag específico del PLC desde memoria M
        
        Args:
            tag_name (str): Nombre del tag a leer
            
        Returns:
            int/float: Valor del tag
        """
        if tag_name not in self.tags_config:
            logger.error(f"Tag {tag_name} no encontrado en configuración")
            return None
        
        try:
            config = self.tags_config[tag_name]
            
            # Leer desde memoria M usando mb_read
            data = self.client.mb_read(config["start"], config["size"])
            
            if config["type"] == "int":
                # Leer como entero de 16 bits
                return get_int(data, 0)
            elif config["type"] == "dint":
                # Leer como entero de 32 bits (double integer)
                return get_dint(data, 0)
            elif config["type"] == "time":
                # Leer como TIME (32 bits = milisegundos)
                time_ms = get_dword(data, 0)
                return time_ms
            elif config["type"] == "bool":
                # Leer como booleano (1 byte, bit específico)
                return snap7.util.get_bool(data, 0, 0)
            else:
                return data
        except Exception as e:
            logger.error(f"Error al leer tag {tag_name}: {e}")
            return None
    
    def read_all_data(self):
        """Lee todos los datos del PLC - las 8 variables principales"""
        data = {}
        
        # Leer todas las variables configuradas
        for tag_name in self.tags_config.keys():
            value = self.read_tag(tag_name)
            if value is not None:
                data[tag_name] = value
                
                # Log especial para variables TIME
                if self.tags_config[tag_name]["type"] == "time":
                    logger.debug(f"{tag_name}: {value} ms ({self.format_time(value)})")
                else:
                    logger.debug(f"{tag_name}: {value}")
        
        # Procesar estado del sistema basado en system_status
        system_status_code = data.get('system_status', 0)
        if system_status_code == 0:
            data['system_status_text'] = 'OK'
            data['error_message'] = ''
        else:
            data['system_status_text'] = 'Error'
            data['error_message'] = self.error_codes.get(system_status_code, f"Error desconocido: {system_status_code}")
        
        # Agregar timestamp
        data['timestamp'] = datetime.now()
        
        return data
    
    def test_connection(self):
        """Prueba la conexión y lee un valor simple"""
        try:
            logger.info("Probando conexión con PLC...")
            if not self.connect_plc():
                return False
            
            # Leer los primeros 4 bytes de memoria M
            data = self.client.mb_read(0, 4)
            test_value = get_byte(data, 0)  # Obtener el primer byte
            logger.info(f"Valor de prueba leído desde M0: {test_value}")
            
            self.disconnect_plc()
            return True
            
        except Exception as e:
            logger.error(f"Error en prueba de conexión: {e}")
            return False
    
    def save_to_firebase(self, data):
        """Guarda los datos en Firebase"""
        if not self.db:
            logger.error("Firebase no está inicializado")
            return False
        
        try:
            # Convertir variables TIME a formato legible antes de guardar
            firebase_data = data.copy()
            for tag_name, config in self.tags_config.items():
                if config["type"] == "time" and tag_name in firebase_data:
                    # Agregar campo formateado
                    firebase_data[f"{tag_name}_formatted"] = self.format_time(firebase_data[tag_name])
            
            collection_ref = self.db.collection(DATABASE_CONFIG["collection_name"])
            collection_ref.add(firebase_data)
            logger.info("Datos guardados en Firebase")
            
            # Limpiar registros antiguos si está habilitado
            if DATABASE_CONFIG.get("auto_cleanup", False):
                self.cleanup_old_records()
            
            return True
        except Exception as e:
            logger.error(f"Error al guardar en Firebase: {e}")
            return False
    
    def cleanup_old_records(self):
        """Limpia registros antiguos para mantener el límite"""
        try:
            collection_ref = self.db.collection(DATABASE_CONFIG["collection_name"])
            
            # Obtener todos los documentos ordenados por timestamp
            docs = collection_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
            
            doc_list = list(docs)
            max_records = DATABASE_CONFIG.get("max_records", 1000)
            
            if len(doc_list) > max_records:
                # Eliminar los registros más antiguos
                for doc in doc_list[max_records:]:
                    doc.reference.delete()
                
                logger.info(f"Limpiados {len(doc_list) - max_records} registros antiguos")
        except Exception as e:
            logger.error(f"Error al limpiar registros: {e}")
    
    def start_monitoring(self, interval=5):
        """
        Inicia el monitoreo continuo del PLC
        
        Args:
            interval (int): Intervalo de lectura en segundos
        """
        if not self.connect_plc():
            logger.error("No se pudo conectar al PLC")
            return
        
        self.running = True
        logger.info(f"Iniciando monitoreo con intervalo de {interval} segundos")
        
        while self.running:
            try:
                # Leer datos del PLC
                data = self.read_all_data()
                
                if data:
                    # Log con formato TIME para las variables correspondientes
                    production_time_str = self.format_time(data.get('production_time', 0)) if data.get('production_time') else 'N/A'
                    active_time_str = self.format_time(data.get('active_time', 0)) if data.get('active_time') else 'N/A'
                    stop_time_str = self.format_time(data.get('stop_time', 0)) if data.get('stop_time') else 'N/A'
                    
                    logger.info(f"Datos leídos: Box Count={data.get('box_count', 'N/A')}, "
                              f"Speed={data.get('machine_speed', 'N/A')}, "
                              f"Status={data.get('system_status', 'N/A')}, "
                              f"Production Time={production_time_str}, "
                              f"Remaining Cycles={data.get('remaining_cycles', 'N/A')}, "
                              f"Cycles={data.get('cycles', 'N/A')}, "
                              f"Active Time={active_time_str}, "
                              f"Stop Time={stop_time_str}")
                    
                    # Guardar en Firebase
                    self.save_to_firebase(data)
                
                # Esperar el intervalo especificado
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("Monitoreo interrumpido por el usuario")
                break
            except Exception as e:
                logger.error(f"Error durante el monitoreo: {e}")
                time.sleep(interval)
        
        self.stop_monitoring()
    
    def stop_monitoring(self):
        """Detiene el monitoreo"""
        self.running = False
        self.disconnect_plc()
        logger.info("Monitoreo detenido")

def main():
    """Función principal para ejecutar el conector"""
    # Configuración del PLC (ajustar según tu setup)
    PLC_IP = input("Ingresa la IP del PLC (Enter para 192.168.5.3): ").strip() or "192.168.5.3"
    RACK = int(input("Ingresa el número de rack (Enter para 0): ").strip() or "0")
    SLOT = int(input("Ingresa el número de slot (Enter para 1): ").strip() or "1")
    MONITORING_INTERVAL = 5    # Intervalo de lectura en segundos
    
    # Crear instancia del conector
    connector = PLCConnector(plc_ip=PLC_IP, rack=RACK, slot=SLOT)
    
    # Primero probar la conexión
    if connector.test_connection():
        print("Conexión exitosa! Iniciando monitoreo...")
        try:
            # Iniciar monitoreo
            connector.start_monitoring(interval=MONITORING_INTERVAL)
        except KeyboardInterrupt:
            print("\nDeteniendo el monitoreo...")
            connector.stop_monitoring()
    else:
        print("No se pudo establecer conexión con el PLC")
        print("Verifica:")
        print("- IP del PLC")
        print("- Números de rack y slot")
        print("- Que el PLC esté en modo RUN")
        print("- Que PUT/GET esté habilitado")

if __name__ == "__main__":
    main()

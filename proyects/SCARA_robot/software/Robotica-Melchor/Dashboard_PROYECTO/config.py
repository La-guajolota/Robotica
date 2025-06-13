# config.py
import os
from firebase_admin import credentials

def get_firebase_config():
    # Opción 1: Usar archivo JSON de credenciales
    if os.path.exists("firebase-credentials.json"):
        return credentials.Certificate("firebase-credentials.json")
    
# Configuración de la base de datos
DATABASE_CONFIG = {
    "collection_name": "plc_data",
    "max_records": 1000,  # Máximo número de registros a mantener
    "auto_cleanup": True  # Limpiar registros antiguos automáticamente
}
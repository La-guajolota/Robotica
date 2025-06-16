# run.py - Script principal de inicio
import subprocess
import threading
import time
import sys
import os

def run_plc_connector():
    """Ejecuta el conector PLC en un hilo separado"""
    try:
        subprocess.run([sys.executable, "/home/pi2/proyecto/guiDB/conector_PLC.py"])
    except Exception as e:
        print(f"Error al ejecutar el conector PLC: {e}")

def run_streamlit_dashboard():
    """Ejecuta el dashboard de Streamlit"""
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", r"/home/pi2/proyecto/guiDB/dashboard.py", "--server.port=8501"])
    except Exception as e:
        print(f"Error al ejecutar Streamlit: {e}")

def main():
    print("🏭 Iniciando Sistema de Monitoreo PLC")
    print("=====================================")
    
    # Verificar que los archivos necesarios existen
    required_files = [r"/home/pi2/proyecto/guiDB/dashboard.py", r"/home/pi2/proyecto/guiDB/config.py"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Error: Archivo {file} no encontrado")
            return
    
    print("✅ Todos los archivos necesarios encontrados")
    
    # Preguntar al usuario qué desea ejecutar
    print("\n¿Qué deseas ejecutar?")
    print("1. Solo Dashboard de Streamlit")
    print("2. Solo Conector PLC")
    print("3. Ambos (Dashboard + Conector PLC)")
    
    choice = input("\nSelecciona una opción (1-3): ").strip()
    
    if choice == "1":
        print("\n🚀 Iniciando Dashboard de Streamlit...")
        print("Accede a: http://localhost:8501")
        run_streamlit_dashboard()
    
    elif choice == "2":
        print("\n🔗 Iniciando Conector PLC...")
        run_plc_connector()
    
    elif choice == "3":
        print("\n🚀 Iniciando ambos servicios...")
        print("Dashboard disponible en: http://localhost:8501")
        
        # Ejecutar conector PLC en hilo separado
        plc_thread = threading.Thread(target=run_plc_connector, daemon=True)
        plc_thread.start()
        
        # Esperar un poco antes de iniciar Streamlit
        time.sleep(2)
        
        # Ejecutar Streamlit en el hilo principal
        run_streamlit_dashboard()
    
    else:
        print("❌ Opción no válida")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")

# run.bat - Script para Windows
"""
@echo off
echo 🏭 Iniciando Sistema de Monitoreo PLC
echo =====================================
python run.py
pause
"""

# run.sh - Script para Linux/Mac
"""
#!/bin/bash
echo "🏭 Iniciando Sistema de Monitoreo PLC"
echo "====================================="
python3 run.py
"""


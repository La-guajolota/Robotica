"""
Demo simple para transmitir una imagen desde Raspberry Pi headless
"""

from flask import Flask, render_template, jsonify
import cv2
import base64
import threading
import time
import numpy as np

app = Flask(__name__)

# Variables globales
current_frame = None
frame_lock = threading.Lock()
camera_status = "Desconectada"

def frame_to_base64(frame):
    """
    Convierte un frame de OpenCV a base64 para transmisión web
    """
    if frame is None:
        return None
    
    # Codificar frame como JPEG
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    
    # Convertir a base64
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    return frame_base64

def load_static_image():
    """
    Carga una imagen estática como fallback
    """
    static_image_path = "/home/pi/emplayadora/tests/demo_image.jpg"  # Nombre del archivo de imagen
    
    try:
        # Intentar cargar imagen guardada
        frame = cv2.imread(static_image_path)
        if frame is not None:
            print(f"✅ Imagen estática cargada: {static_image_path}")
            return frame
    except Exception as e:
        print(f"⚠️  No se pudo cargar imagen estática: {e}")
    
    # Si no hay imagen, crear una imagen de prueba
    print("🎨 Creando imagen de prueba...")
    frame = create_test_image()
    return frame

def create_test_image():
    """
    Crea una imagen de prueba si no hay cámara ni imagen guardada
    """
    # Crear imagen de 640x480 con fondo azul
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    frame[:] = (100, 50, 0)  # Fondo azul oscuro
    
    # Agregar texto y elementos gráficos
    cv2.putText(frame, "RASPBERRY PI DEMO", (120, 100), 
               cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
    cv2.putText(frame, "No hay camara detectada", (160, 150), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(frame, "Usando imagen estatica", (170, 190), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    
    # Agregar rectángulo decorativo
    cv2.rectangle(frame, (50, 250), (590, 400), (255, 255, 255), 2)
    cv2.putText(frame, "Coloca tu imagen en:", (80, 290), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, "demo_image.jpg", (200, 330), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, "en la misma carpeta del script", (120, 370), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    return frame

def camera_thread():
    """
    Hilo para capturar frames de la cámara o mostrar imagen estática
    """
    global current_frame, camera_status
    
    print("🔄 Intentando conectar con la cámara...")
    
    # Intentar conectar con la cámara
    cap = cv2.VideoCapture(0)  # Cámara 0
    
    if not cap.isOpened():
        print("❌ No se detectó cámara, usando imagen estática")
        camera_status = "Imagen estática"
        
        # Cargar imagen estática
        static_frame = load_static_image()
        frame_count = 0
        
        while True:
            frame_count += 1
            frame = static_frame.copy()
            
            # Agregar información dinámica a la imagen estática
            cv2.putText(frame, f"Frame: {frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, time.strftime("%Y-%m-%d %H:%M:%S"), (10, 450), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            # Actualizar frame global
            with frame_lock:
                current_frame = frame.copy()
                camera_status = "Imagen estática activa"
            
            time.sleep(1)  # Actualizar cada segundo para imagen estática
        
        return
    
    # Si hay cámara, continuar con el flujo normal
    # Configurar cámara
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 10)
    
    print("✅ Cámara conectada exitosamente")
    camera_status = "Conectada"
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("⚠️  No se pudo capturar frame, cambiando a imagen estática")
            camera_status = "Error - Cambiando a imagen estática"
            cap.release()
            
            # Cambiar a imagen estática
            static_frame = load_static_image()
            while True:
                frame_count += 1
                frame = static_frame.copy()
                
                cv2.putText(frame, f"Frame: {frame_count}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, time.strftime("%Y-%m-%d %H:%M:%S"), (10, 450), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                with frame_lock:
                    current_frame = frame.copy()
                    camera_status = "Imagen estática (cámara falló)"
                
                time.sleep(1)
            
            return
        
        frame_count += 1
        
        # Agregar información al frame de cámara
        cv2.putText(frame, f"Frame: {frame_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Raspberry Pi Demo", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(frame, time.strftime("%Y-%m-%d %H:%M:%S"), (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Actualizar frame global con thread safety
        with frame_lock:
            current_frame = frame.copy()
            camera_status = "Transmitiendo desde cámara"
        
        time.sleep(0.1)  # Control de FPS (~10 FPS)
    
    cap.release()

@app.route('/')
def index():
    """
    Página principal con la interfaz web
    """
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🍓 Raspberry Pi Camera Demo</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                text-align: center;
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            .status-box {
                background: rgba(255,255,255,0.1);
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                backdrop-filter: blur(10px);
            }
            .video-container {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }
            #camera-feed {
                max-width: 100%;
                height: auto;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            }
            .info {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .info-card {
                background: rgba(255,255,255,0.1);
                padding: 15px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
            .status-connected { color: #4CAF50; }
            .status-error { color: #f44336; }
            .status-loading { color: #FF9800; }
            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid rgba(255,255,255,.3);
                border-radius: 50%;
                border-top-color: #fff;
                animation: spin 1s ease-in-out infinite;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🍓 Raspberry Pi Camera Demo</h1>
            
            <div class="status-box">
                <h3>📡 Estado de la Cámara</h3>
                <p><strong>Estado:</strong> <span id="camera-status" class="status-loading">Conectando... <div class="loading"></div></span></p>
                <p><strong>Última actualización:</strong> <span id="last-update">--</span></p>
            </div>

            <div class="video-container">
                <h3>📹 Transmisión en Vivo</h3>
                <img id="camera-feed" src="" alt="Esperando señal de cámara..." style="display: none;">
                <div id="no-signal" style="padding: 60px; color: rgba(255,255,255,0.7);">
                    <div class="loading" style="margin-bottom: 20px;"></div>
                    <p>Esperando señal de cámara...</p>
                </div>
            </div>

            <div class="info">
                <div class="info-card">
                    <h4>🔧 Información Técnica</h4>
                    <p><strong>Resolución:</strong> 640x480</p>
                    <p><strong>FPS:</strong> ~10</p>
                    <p><strong>Puerto:</strong> 5000</p>
                </div>
                <div class="info-card">
                    <h4>🎯 Instrucciones</h4>
                    <p>Esta es una transmisión en vivo desde tu Raspberry Pi</p>
                    <p>La imagen se actualiza automáticamente</p>
                </div>
            </div>
        </div>

        <script>
            let frameCount = 0;
            
            function updateCamera() {
                fetch('/get_frame')
                    .then(response => response.json())
                    .then(data => {
                        const statusElement = document.getElementById('camera-status');
                        const feedElement = document.getElementById('camera-feed');
                        const noSignalElement = document.getElementById('no-signal');
                        const lastUpdateElement = document.getElementById('last-update');
                        
                        if (data.frame) {
                            // Mostrar imagen
                            feedElement.src = 'data:image/jpeg;base64,' + data.frame;
                            feedElement.style.display = 'block';
                            noSignalElement.style.display = 'none';
                            
                            // Actualizar estado
                            statusElement.innerHTML = '<span class="status-connected">✅ ' + data.status + '</span>';
                            lastUpdateElement.textContent = new Date().toLocaleTimeString();
                            frameCount++;
                        } else {
                            // Sin señal
                            feedElement.style.display = 'none';
                            noSignalElement.style.display = 'block';
                            statusElement.innerHTML = '<span class="status-error">❌ ' + data.status + '</span>';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('camera-status').innerHTML = '<span class="status-error">❌ Error de conexión</span>';
                        document.getElementById('camera-feed').style.display = 'none';
                        document.getElementById('no-signal').style.display = 'block';
                    });
            }

            // Actualizar cada 100ms para ~10 FPS
            setInterval(updateCamera, 100);
            
            // Cargar inicial
            updateCamera();
        </script>
    </body>
    </html>
    '''

@app.route('/get_frame')
def get_frame():
    """
    API endpoint para obtener el frame actual
    """
    global current_frame, camera_status
    
    with frame_lock:
        if current_frame is not None:
            frame_b64 = frame_to_base64(current_frame)
            return jsonify({
                'frame': frame_b64,
                'status': camera_status,
                'timestamp': time.time()
            })
    
    return jsonify({
        'frame': None,
        'status': camera_status,
        'timestamp': time.time()
    })

def main():
    """
    Función principal
    """
    print("🚀 Iniciando Demo de Cámara Raspberry Pi")
    print("=" * 50)
    
    # Iniciar hilo de cámara
    camera_thread_obj = threading.Thread(target=camera_thread, daemon=True)
    camera_thread_obj.start()
    
    print("📷 Hilo de cámara/imagen iniciado")
    print("🌐 Iniciando servidor web...")
    print("\n💡 INSTRUCCIONES:")
    print("1. Encuentra la IP de tu Raspberry Pi: hostname -I")
    print("2. Abre tu navegador y ve a: http://TU_IP:5000")
    print("3. Por ejemplo: http://192.168.1.100:5000")
    print("\n📸 PARA USAR TU PROPIA IMAGEN:")
    print("1. Guarda tu imagen como 'demo_image.jpg' en esta carpeta")
    print("2. Formatos soportados: JPG, PNG, BMP")
    print("3. Resolución recomendada: 640x480 o similar")
    print("\n🛑 Presiona Ctrl+C para detener")
    print("=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor...")

if __name__ == "__main__":
    main()  
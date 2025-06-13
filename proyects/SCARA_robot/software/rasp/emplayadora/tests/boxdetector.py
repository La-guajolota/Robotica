"""
Raspberry Pi Object Measurement Stream - Headless Version
Streaming web ligero con medición de objetos en tiempo real
"""

from flask import Flask, Response, render_template_string, jsonify
import cv2
import threading
import time
import logging
import numpy as np
from scipy.spatial import distance as dist
from imutils import perspective, contours
import imutils
import signal
import sys
import os

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

class ObjectMeasurementStreamer:
    def __init__(self):
        self.camera = None
        self.frame = None
        self.processed_frame = None
        self.lock = threading.Lock()
        self.running = False
        
        # Configuraciones optimizadas para Raspberry Pi
        self.fps = 10  # FPS reducido para mejor rendimiento
        self.width = 640
        self.height = 480
        self.quality = 75  # Calidad JPEG balanceada
        
        # Variables de medición
        self.pixels_per_metric = None
        self.measurement_enabled = True
        self.show_edges = False
        
        # Estadísticas
        self.frame_count = 0
        self.processing_time = 0
        
    def midpoint(self, ptA, ptB):
        """Calcular punto medio entre dos puntos"""
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
    
    def initialize_camera(self):
        """Inicializar cámara USB con configuraciones optimizadas"""
        logger.info("🔍 Buscando cámara USB...")
        
        for camera_index in range(3):
            try:
                logger.info(f"Probando cámara en índice {camera_index}")
                cap = cv2.VideoCapture(camera_index)
                
                if cap.isOpened():
                    # Configuraciones optimizadas
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                    cap.set(cv2.CAP_PROP_FPS, self.fps)
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    
                    # Test de funcionamiento
                    ret, test_frame = cap.read()
                    if ret and test_frame is not None:
                        logger.info(f"✅ Cámara USB encontrada en índice {camera_index}")
                        self.camera = cap
                        return True
                    
                cap.release()
                
            except Exception as e:
                logger.warning(f"Error probando cámara {camera_index}: {e}")
                continue
        
        logger.error("❌ No se encontró cámara USB funcional")
        return False
    
    def measure_objects(self, cnts, image):
        """Medir dimensiones de objetos basado en contornos"""
        results = []
        
        for c in cnts:
            # Ignorar contornos pequeños
            area = cv2.contourArea(c)
            if area < 500:  # Área mínima ajustable
                continue
            
            try:
                # Calcular bounding box rotado
                box = cv2.minAreaRect(c)
                box = cv2.boxPoints(box)
                box = np.array(box, dtype="int")
                box = perspective.order_points(box)
                
                results.append((box, area))
                
            except Exception as e:
                logger.warning(f"Error procesando contorno: {e}")
                continue
        
        return results
    
    def draw_measurements(self, image, measurements):
        """Dibujar mediciones en la imagen"""
        for i, (box, area) in enumerate(measurements):
            # Dibujar contorno
            cv2.drawContours(image, [box.astype("int")], -1, (0, 255, 0), 2)
            
            # Dibujar puntos de esquina
            for (x, y) in box:
                cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)
            
            # Calcular puntos medios
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = self.midpoint(tl, tr)
            (blbrX, blbrY) = self.midpoint(bl, br)
            (tlblX, tlblY) = self.midpoint(tl, bl)
            (trbrX, trbrY) = self.midpoint(tr, br)
            
            # Dibujar puntos medios
            for (x, y) in [(tltrX, tltrY), (blbrX, blbrY), (tlblX, tlblY), (trbrX, trbrY)]:
                cv2.circle(image, (int(x), int(y)), 5, (255, 0, 0), -1)
            
            # Dibujar líneas de medición
            cv2.line(image, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
            cv2.line(image, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)
            
            # Calcular distancias
            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
            
            # Calibración automática si no existe
            if self.pixels_per_metric is None:
                self.pixels_per_metric = dB / 10  # 10 unidades como referencia
            
            # Calcular dimensiones
            dimA = dA / self.pixels_per_metric
            dimB = dB / self.pixels_per_metric
            
            # Mostrar dimensiones
            cv2.putText(image, f"{dimA:.1f}u", 
                       (int(tltrX - 15), int(tltrY - 10)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(image, f"{dimB:.1f}u", 
                       (int(trbrX + 10), int(trbrY)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Mostrar área
            cv2.putText(image, f"Area: {area:.0f}px", 
                       (int(tlblX), int(tlblY + 20)),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        return image
    
    def process_frame(self, frame):
        """Procesar frame para detección y medición de objetos"""
        start_time = time.time()
        
        if not self.measurement_enabled:
            return frame
        
        try:
            # Preprocesamiento optimizado
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)  # Blur reducido para mejor rendimiento
            
            # Detección de bordes
            edged = cv2.Canny(gray, 50, 100)
            edged = cv2.dilate(edged, None, iterations=1)
            edged = cv2.erode(edged, None, iterations=1)
            
            # Encontrar contornos
            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            
            if len(cnts) > 0:
                cnts, _ = contours.sort_contours(cnts)
                measurements = self.measure_objects(cnts, frame)
                
                if measurements:
                    frame = self.draw_measurements(frame, measurements)
            
            # Mostrar información en pantalla
            info_text = f"Objetos: {len(cnts)} | FPS: {1/(time.time()-start_time):.1f}"
            cv2.putText(frame, info_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Guardar tiempo de procesamiento
            self.processing_time = time.time() - start_time
            
        except Exception as e:
            logger.error(f"Error procesando frame: {e}")
        
        return frame
    
    def camera_thread(self):
        """Hilo principal de captura y procesamiento"""
        logger.info("🎬 Iniciando hilo de cámara...")
        
        while self.running:
            if self.camera is None or not self.camera.isOpened():
                time.sleep(1)
                continue
            
            ret, frame = self.camera.read()
            
            if not ret or frame is None:
                logger.warning("Frame perdido")
                continue
            
            # Procesar frame
            processed = self.process_frame(frame.copy())
            
            # Actualizar frames con thread safety
            with self.lock:
                self.frame = frame.copy()
                self.processed_frame = processed.copy()
                self.frame_count += 1
            
            # Control de FPS
            time.sleep(1.0 / self.fps)
    
    def generate_stream(self, show_processed=True):
        """Generador de stream MJPEG"""
        while self.running:
            with self.lock:
                if show_processed and self.processed_frame is not None:
                    frame = self.processed_frame.copy()
                elif self.frame is not None:
                    frame = self.frame.copy()
                else:
                    continue
            
            # Codificar frame como JPEG
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
            result, encimg = cv2.imencode('.jpg', frame, encode_param)
            
            if not result:
                continue
            
            # Generar stream MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + 
                   encimg.tobytes() + b'\r\n')
    
    def start(self):
        """Iniciar el streamer"""
        if not self.initialize_camera():
            return False
        
        self.running = True
        self.thread = threading.Thread(target=self.camera_thread, daemon=True)
        self.thread.start()
        return True
    
    def stop(self):
        """Detener el streamer"""
        self.running = False
        if self.camera:
            self.camera.release()

# Instancia global del streamer
streamer = ObjectMeasurementStreamer()

# Plantilla HTML optimizada y ligera
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🍓 Pi Object Measurement</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 15px;
            background: #1a1a1a;
            color: white;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .video-container {
            text-align: center;
            margin: 20px 0;
        }
        .stream {
            max-width: 100%;
            border: 2px solid #4CAF50;
            border-radius: 8px;
        }
        .controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        .btn:hover { background: #45a049; }
        .btn.secondary { background: #2196F3; }
        .btn.secondary:hover { background: #1976D2; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .instructions {
            background: rgba(76,175,80,0.1);
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .instructions h3 { margin-top: 0; }
        .instructions ul { margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍓 Raspberry Pi Object Measurement</h1>
        
        <div class="video-container">
            <img id="stream" class="stream" src="/video_feed" alt="Camera Stream">
        </div>
        
        <div class="controls">
            <button class="btn" onclick="toggleMeasurement()">📏 Toggle Measurement</button>
            <button class="btn secondary" onclick="resetCalibration()">🔄 Reset Calibration</button>
            <button class="btn secondary" onclick="switchView()">👁️ Switch View</button>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h4>📊 Statistics</h4>
                <p>Frames: <span id="frames">0</span></p>
                <p>Processing: <span id="processing">0</span>ms</p>
            </div>
            <div class="stat-card">
                <h4>⚙️ Settings</h4>
                <p>Resolution: 640x480</p>
                <p>Quality: 75%</p>
                <p>FPS Target: 10</p>
            </div>
        </div>
        
        <div class="instructions">
            <h3>📋 Instructions</h3>
            <ul>
                <li><strong>Measurement:</strong> Place objects with clear edges in view</li>
                <li><strong>Calibration:</strong> First object sets the reference scale (10 units)</li>
                <li><strong>Units:</strong> Measurements shown in relative units</li>
                <li><strong>Performance:</strong> Optimized for Raspberry Pi headless operation</li>
            </ul>
        </div>
    </div>

    <script>
        let showProcessed = true;
        
        function toggleMeasurement() {
            fetch('/toggle_measurement', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    console.log('Measurement toggled:', data.enabled);
                });
        }
        
        function resetCalibration() {
            fetch('/reset_calibration', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    console.log('Calibration reset');
                });
        }
        
        function switchView() {
            showProcessed = !showProcessed;
            const stream = document.getElementById('stream');
            stream.src = showProcessed ? '/video_feed' : '/raw_feed';
        }
        
        function updateStats() {
            fetch('/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('frames').textContent = data.frames;
                    document.getElementById('processing').textContent = data.processing_time.toFixed(1);
                });
        }
        
        // Actualizar estadísticas cada 2 segundos
        setInterval(updateStats, 2000);
        updateStats();
    </script>
</body>
</html>
'''

# Rutas Flask
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    return Response(streamer.generate_stream(show_processed=True),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/raw_feed')
def raw_feed():
    return Response(streamer.generate_stream(show_processed=False),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_measurement', methods=['POST'])
def toggle_measurement():
    streamer.measurement_enabled = not streamer.measurement_enabled
    return jsonify({'enabled': streamer.measurement_enabled})

@app.route('/reset_calibration', methods=['POST'])
def reset_calibration():
    streamer.pixels_per_metric = None
    return jsonify({'reset': True})

@app.route('/stats')
def get_stats():
    return jsonify({
        'frames': streamer.frame_count,
        'processing_time': streamer.processing_time * 1000,  # en ms
        'measurement_enabled': streamer.measurement_enabled
    })

def signal_handler(sig, frame):
    """Manejo de señales para cierre limpio"""
    logger.info("🛑 Deteniendo servidor...")
    streamer.stop()
    sys.exit(0)

def main():
    """Función principal"""
    print("🚀 Raspberry Pi Object Measurement Stream")
    print("=" * 50)
    
    # Registrar manejador de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Iniciar streamer
    if not streamer.start():
        print("❌ Error: No se pudo inicializar la cámara")
        return
    
    print("✅ Cámara inicializada correctamente")
    print("🌐 Iniciando servidor web...")
    print("\n💡 INSTRUCCIONES:")
    print("1. Encuentra la IP de tu Raspberry Pi: hostname -I")
    print("2. Abre tu navegador y ve a: http://TU_IP:5000")
    print("3. Ejemplo: http://192.168.1.100:5000")
    print("\n📏 MEDICIÓN DE OBJETOS:")
    print("- Coloca objetos con bordes claros en el campo de visión")
    print("- El primer objeto establecerá la escala de calibración")
    print("- Las medidas se muestran en unidades relativas")
    print("\n🛑 Presiona Ctrl+C para detener")
    print("=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor...")
    finally:
        streamer.stop()

if __name__ == "__main__":
    main()

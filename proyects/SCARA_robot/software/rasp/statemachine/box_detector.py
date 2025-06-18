# box_detector.py
import cv2
import threading
import time
import requests 
import base64
import signal
import sys
from console_styler import styler

# Configuración del Servidor PC
PC_SERVER_URL = "http://192.168.0.118:5001"  # Cambia a la IP de tu PC

class BoxDetector:
    def __init__(self):
        # Configuración de la cámara
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            styler.print("Error: No se pudo abrir la cámara.", "error", "red", bold=True)
            sys.exit(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Parámetros de detección
        self.min_area = 1000
        self.max_area = 50000
        self.aspect_ratio_range = (0.5, 2.0)
        
        # Variables de estado
        self.box_detected = False
        self.box_height = 0
        self.box_width = 0
        self.box_area = 0
        
        # Hilos
        self.running = False
        self.detection_thread = None
        self.lock = threading.Lock()
        
    def detect_boxes(self, frame):
        """Detecta cajas rectangulares en un fotograma."""
        processed = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        box_detected_flag = False
        measurements = {'height': 0, 'width': 0, 'area': 0}
        
        if contours:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            for contour in contours:
                area = cv2.contourArea(contour)
                if self.min_area < area < self.max_area:
                    epsilon = 0.02 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)
                    if len(approx) == 4:
                        (x, y, w, h) = cv2.boundingRect(approx)
                        aspect_ratio = float(w) / h
                        if self.aspect_ratio_range[0] <= aspect_ratio <= self.aspect_ratio_range[1]:
                            cv2.drawContours(processed, [approx], -1, (0, 255, 0), 3)
                            box_detected_flag = True
                            measurements = {'height': h, 'width': w, 'area': area}
                            break
        
        return box_detected_flag, processed, measurements

    def send_to_server(self, original_frame, processed_frame, detected, measurements):
        """Envía datos e imágenes al servidor del PC."""
        try:
            _, buffer_orig = cv2.imencode('.jpg', original_frame)
            original_b64 = base64.b64encode(buffer_orig).decode('utf-8')
            
            _, buffer_proc = cv2.imencode('.jpg', processed_frame)
            processed_b64 = base64.b64encode(buffer_proc).decode('utf-8')
            
            payload = {
                'box_detected': detected,
                'measurements': measurements,
                'original_image': original_b64,
                'processed_image': processed_b64
            }
            
            requests.post(f"{PC_SERVER_URL}/detector_data", json=payload, timeout=3.0)
            
        except requests.exceptions.RequestException as e:
            styler.print(f"Error enviando datos al PC: {e}", "error", "red")

    def detection_loop(self):
        """Bucle principal de detección que se ejecuta en un hilo."""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue
            
            detected, processed, measurements = self.detect_boxes(frame)
            
            with self.lock:
                self.box_detected = detected
                self.box_height = measurements['height']
                self.box_width = measurements['width']
                self.box_area = measurements['area']

            self.send_to_server(frame, processed, detected, measurements)
            time.sleep(0.5)

    def start_detection(self):
        """Inicia el sistema de detección."""
        if not self.running:
            self.running = True
            self.detection_thread = threading.Thread(target=self.detection_loop)
            self.detection_thread.daemon = True
            self.detection_thread.start()
            styler.print("Detección de cajas iniciada.", "play", "green")
    
    def stop_detection(self):
        """Detiene el sistema de detección."""
        if self.running:
            self.running = False
            if self.detection_thread:
                self.detection_thread.join()
            styler.print("Detección de cajas detenida.", "stop", "yellow")
    
    def cleanup(self):
        """Libera los recursos."""
        self.stop_detection()
        if self.cap:
            self.cap.release()
    
    def is_box_present(self):
        """Verifica si se detecta una caja."""
        with self.lock:
            return self.box_detected
    
    def get_box_measurements(self):
        """Obtiene las medidas de la caja."""
        with self.lock:
            return {'height': self.box_height, 'width': self.box_width, 'area': self.box_area}

# --- Funciones de Integración ---

# Instancia global
detector_instance = None

def initialize_box_detector():
    """Inicializa el sistema de detección de cajas."""
    global detector_instance
    if detector_instance is None:
        styler.print("Inicializando el detector de cajas...", "camera", "cyan")
        detector_instance = BoxDetector()
        detector_instance.start_detection()
    return detector_instance

def cleanup_box_detector():
    """Limpia los recursos del detector."""
    global detector_instance
    if detector_instance:
        detector_instance.cleanup()

def detect_box():
    """Verifica si hay una caja presente."""
    global detector_instance
    if detector_instance:
        return detector_instance.is_box_present()
    return False

def get_box_height():
    """Obtiene la altura de la caja."""
    global detector_instance
    if detector_instance:
        measurements = detector_instance.get_box_measurements()
        return measurements['height']
    return 0

def request_scara_put_routine():
    """Solicita a SCARA que coloque una caja."""
    try:
        response = requests.post(f"{PC_SERVER_URL}/scara/put_request", timeout=3.0)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        styler.print(f"Error en la solicitud PUT de SCARA: {e}", "error", "red")
        return False

def request_scara_get_routine():
    """Solicita a SCARA que retire una caja."""
    try:
        response = requests.post(f"{PC_SERVER_URL}/scara/get_request", timeout=3.0)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        styler.print(f"Error en la solicitud GET de SCARA: {e}", "error", "red")
        return False

def is_put_routine_done():
    """Verifica si la rutina PUT de SCARA ha finalizado."""
    try:
        response = requests.get(f"{PC_SERVER_URL}/scara/put_status", timeout=3.0)
        if response.status_code == 200:
            return response.json().get('done', False)
    except requests.exceptions.RequestException:
        return False

def is_get_routine_done():
    """Verifica si la rutina GET de SCARA ha finalizado."""
    try:
        response = requests.get(f"{PC_SERVER_URL}/scara/get_status", timeout=3.0)
        if response.status_code == 200:
            return response.json().get('done', False)
    except requests.exceptions.RequestException:
        return False

# --- Bloque para ejecución como script independiente ---
if __name__ == "__main__":
    styler.print_title("Detector de Cajas - Modo de Prueba Independiente", color="blue")
    
    # Inicializar el detector
    initialize_box_detector()
    
    def signal_handler(sig, frame):
        """Manejador para una parada limpia con Ctrl+C."""
        styler.print("\nApagando el detector de cajas...", "bye", "yellow", bold=True)
        cleanup_box_detector()
        sys.exit(0)

    # Registrar el manejador de señales
    signal.signal(signal.SIGINT, signal_handler)
    
    styler.print("El detector está funcionando. Presiona Ctrl+C para salir.", "info", "white")
    
    # Mantener el script principal en ejecución para que el hilo de detección pueda funcionar
    while True:
        # Aquí puedes agregar impresiones de estado si lo deseas
        if detector_instance:
            detected = detector_instance.is_box_present()
            medidas = detector_instance.get_box_measurements()
            styler.print(f"Estado: {'Caja Detectada' if detected else 'Sin Caja'} | Medidas: {medidas}", "debug")
        time.sleep(2)

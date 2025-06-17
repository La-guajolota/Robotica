import cv2
import threading
import time
import requests 
import base64
import json
import signal
import sys

# --- MODIFICADO: IP de la PC que corre el servidor bridge de ROS2 ---
PC_SERVER_URL = "http://192.168.1.39:5001" # ¡¡¡CAMBIA ESTA IP POR LA DE TU PC!!!

class BoxDetector:
    def __init__(self):
        # Configuración de la cámara
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            sys.exit(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Parámetros de detección
        self.min_area = 1000
        self.max_area = 50000
        self.aspect_ratio_range = (0.5, 2.0)
        
        # Almacenamiento de datos
        self.box_detected = False
        self.box_height = 0
        self.box_width = 0
        self.box_area = 0
        
        # Threading
        self.running = False
        self.detection_thread = None
        self.lock = threading.Lock()
        
    def detect_boxes(self, frame):
        """Detecta cajas rectangulares en el frame (sin cambios en la lógica de CV)."""
        processed = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        cnts, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        box_detected = False
        box_measurements = {'height': 0, 'width': 0, 'area': 0}
        
        if len(cnts) > 0:
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
            for contour in cnts:
                area = cv2.contourArea(contour)
                if not (self.min_area < area < self.max_area):
                    continue
                
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                if len(approx) == 4:
                    (x, y, w, h) = cv2.boundingRect(approx)
                    aspect_ratio = float(w) / h
                    if not (self.aspect_ratio_range[0] <= aspect_ratio <= self.aspect_ratio_range[1]):
                        continue
                        
                    cv2.drawContours(processed, [approx], -1, (0, 255, 0), 3)
                    box_detected = True
                    box_measurements = {'height': h, 'width': w, 'area': area}
                    break # Se encontró una caja válida
        
        return box_detected, processed, box_measurements

    def send_to_pc_server(self, original_frame, processed_frame, detected, measurements):
        """
        --- NUEVA FUNCIÓN ---
        Envía los datos e imágenes al servidor en la PC.
        """
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
            
            requests.post(f"{PC_SERVER_URL}/detector_data", json=payload, timeout=1.0)
            
        except requests.exceptions.RequestException as e:
            print(f"Error al enviar datos a la PC: {e}")

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

            # Envía los datos al servidor en la PC
            self.send_to_pc_server(frame, processed, detected, measurements)
            
            time.sleep(0.1)  # ~10 FPS

    def start_detection(self):
        """Inicia el sistema de detección."""
        if not self.running:
            self.running = True
            self.detection_thread = threading.Thread(target=self.detection_loop)
            self.detection_thread.daemon = True
            self.detection_thread.start()
            print("Detección de cajas iniciada.")
    
    def stop_detection(self):
        """Detiene el sistema de detección."""
        self.running = False
        if self.detection_thread:
            self.detection_thread.join()
        print("Detección de cajas detenida.")
    
    def cleanup(self):
        """Libera los recursos."""
        self.stop_detection()
        if self.cap:
            self.cap.release()
    
    # --- Funciones públicas para la integración con la máquina de estados ---
    def is_box_present(self):
        with self.lock:
            return self.box_detected
    
    def get_box_measurements(self):
        with self.lock:
            return {'height': self.box_height, 'width': self.box_width, 'area': self.box_area}

# --- Instancia global para ser usada por otros módulos ---
detector_instance = None

def initialize_box_detector():
    """Inicializa el sistema de detección de cajas."""
    global detector_instance
    if detector_instance is None:
        detector_instance = BoxDetector()
        detector_instance.start_detection()
    return detector_instance

def cleanup_box_detector():
    """Limpia los recursos del detector de cajas."""
    global detector_instance
    if detector_instance:
        detector_instance.cleanup()

# --- Funciones de integración para la máquina de estados ---

def detect_box():
    """Función para que la máquina de estados verifique la presencia de una caja."""
    global detector_instance
    if detector_instance:
        return detector_instance.is_box_present()
    return False

def get_box_height():
    """Función para que la máquina de estados obtenga la altura de la caja."""
    global detector_instance
    if detector_instance:
        measurements = detector_instance.get_box_measurements()
        return measurements['height']
    return 0

def request_scara_put_routine():
    """Solicita al SCARA (a través de la PC) que ponga una caja."""
    try:
        response = requests.post(f"{PC_SERVER_URL}/scara/put_request", timeout=1.0)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud PUT a SCARA: {e}")
        return False

def request_scara_get_routine():
    """Solicita al SCARA (a través de la PC) que retire una caja."""
    try:
        response = requests.post(f"{PC_SERVER_URL}/scara/get_request", timeout=1.0)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud GET a SCARA: {e}")
        return False

def is_put_routine_done():
    """Verifica (a través de la PC) si la rutina PUT del SCARA ha terminado."""
    try:
        response = requests.get(f"{PC_SERVER_URL}/scara/put_status", timeout=1.0)
        if response.status_code == 200:
            return response.json().get('done', False)
    except requests.exceptions.RequestException as e:
        print(f"Error al verificar estado de PUT: {e}")
    return False

def is_get_routine_done():
    """Verifica (a través de la PC) si la rutina GET del SCARA ha terminado."""
    try:
        response = requests.get(f"{PC_SERVER_URL}/scara/get_status", timeout=1.0)
        if response.status_code == 200:
            return response.json().get('done', False)
    except requests.exceptions.RequestException as e:
        print(f"Error al verificar estado de GET: {e}")
    return False


if __name__ == "__main__":
    # Este bloque es solo para pruebas directas en la Pi
    print("Iniciando detector de cajas en modo de prueba...")
    initialize_box_detector()
    
    def signal_handler(sig, frame):
        print('\nApagando el detector de cajas...')
        cleanup_box_detector()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    
    # Mantener el script corriendo para que el hilo de detección funcione
    while True:
        time.sleep(1)
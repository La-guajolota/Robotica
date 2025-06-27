# box_detector.py
import cv2
import numpy as np
import threading
import time
import requests 
import base64
import signal
import sys
from console_styler import styler

# --- Server Configuration ---
# Server URLs for different network environments.
dongle_wifi = "http://192.168.0.118:5001"
universidad = "http://10.230.4.56:5001"  
PC_SERVER_URL = universidad  # Set the active server URL here.

# --- Calibration Parameters ---
CALIBRATION_PARAMS = {
    'min_contour_area': 500,       # Minimum area for shape detection
    'max_contour_area': 15000,     # Maximum area for shape detection
    'approx_epsilon': 0.02,        # Contour approximation precision
    'black_lower': [0, 10, 10],      # Lower HSV threshold for black
    'black_upper': [180, 255, 50], # Upper HSV threshold for black
    'kernel_size': (3, 3)          # Kernel size for morphological operations
}

# --- Shape Configuration ---
# Define box heights for each detected shape
SHAPE_HEIGHTS = {
    'square': 10,      # cm
    'circle': 20,      # cm
    'triangle': 10     # cm
}

class BoxDetector:
    """Manages camera operations, detects geometric shapes on boxes, and sends data to a server."""
    
    def __init__(self):
        """Initializes the camera, detection parameters, and state variables."""
        # Camera setup
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            styler.print("Error: Could not open camera.", "error", "red", bold=True)
            sys.exit(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Load calibration parameters
        self.min_contour_area = CALIBRATION_PARAMS['min_contour_area']
        self.max_contour_area = CALIBRATION_PARAMS['max_contour_area']
        self.approx_epsilon = CALIBRATION_PARAMS['approx_epsilon']
        self.black_lower = np.array(CALIBRATION_PARAMS['black_lower'])
        self.black_upper = np.array(CALIBRATION_PARAMS['black_upper'])
        self.kernel_size = CALIBRATION_PARAMS['kernel_size']
        
        # State variables
        self.box_detected = False
        self.detected_shape = None
        self.box_height = 0
        self.box_width = 0
        self.box_area = 0
        
        # Threading components
        self.running = False
        self.detection_thread = None
        self.lock = threading.Lock()
        
    def detect_black_shapes(self, frame):
        """
        Detects black geometric shapes (square, circle, triangle) drawn on boxes.
        
        Args:
            frame: The input image frame from the camera.
            
        Returns:
            A tuple containing:
            - A boolean flag indicating if a shape was detected.
            - The processed frame with shapes highlighted.
            - A dictionary with the shape's measurements and type.
        """
        processed = frame.copy()
        
        # Convert to HSV for better black color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for black color (marker drawings)
        mask = cv2.inRange(hsv, self.black_lower, self.black_upper)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones(self.kernel_size, np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours of black shapes
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        shape_detected_flag = False
        measurements = {'height': 0, 'width': 0, 'area': 0, 'shape': None}
        
        if contours:
            # Sort contours by area in descending order
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                if self.min_contour_area < area < self.max_contour_area:
                    # Get bounding rectangle
                    (x, y, w, h) = cv2.boundingRect(contour)
                    
                    # Classify the shape
                    detected_shape = self.classify_shape(contour)
                    
                    if detected_shape:
                        # Draw the detected shape
                        cv2.drawContours(processed, [contour], -1, (0, 255, 0), 3)
                        
                        # Add label
                        label = f"{detected_shape.upper()}"
                        cv2.putText(processed, label, (x, y-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        
                        # Get assigned height for this shape
                        assigned_height = SHAPE_HEIGHTS.get(detected_shape, 0)
                        
                        shape_detected_flag = True
                        measurements = {
                            'height': assigned_height,  # Use predefined height based on shape
                            'width': w, 
                            'area': area, 
                            'shape': detected_shape
                        }
                        
                        styler.print(f"Detected {detected_shape} - Assigned height: {assigned_height}cm", 
                                   "success", "green")
                        break  # Stop after finding the first valid shape
        
        return shape_detected_flag, processed, measurements, mask
    
    def classify_shape(self, contour):
        """
        Classifies a contour into square, circle, or triangle.
        
        Args:
            contour: The contour to classify.
            
        Returns:
            String indicating the shape type or None if unrecognized.
        """
        # Approximate the contour
        epsilon = self.approx_epsilon * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Get the number of vertices
        vertices = len(approx)
        
        # Calculate some properties for better classification
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return None
            
        # Circularity ratio (4π * area / perimeter^2)
        # Perfect circle = 1.0, square ≈ 0.785
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        
        # Classification logic
        if vertices == 3:
            return 'triangle'
        elif vertices == 4:
            # Check if it's roughly square-like
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if 0.7 <= aspect_ratio <= 1.3:  # Roughly square
                return 'square'
        elif vertices > 8 and circularity > 0.7:
            # Many vertices and high circularity suggests a circle
            return 'circle'
        elif 5 <= vertices <= 8 and circularity > 0.6:
            # Could be a roughly drawn circle
            return 'circle'
        
        return None

    def send_to_server(self, original_frame, processed_frame, gray_scale, detected, measurements):
        """
        Encodes images and sends all detection data to the PC server.
        
        Args:
            original_frame: The raw camera frame.
            processed_frame: The frame after processing and drawing contours.
            gray_scale: The grayscale mask used for detection.
            detected: Boolean indicating if a shape was detected.
            measurements: Dictionary of the shape's measurements and type.
        """
        try:
            # Encode images to JPG format and then to base64 strings
            _, buffer_orig = cv2.imencode('.jpg', original_frame)
            original_b64 = base64.b64encode(buffer_orig).decode('utf-8')
            
            _, buffer_proc = cv2.imencode('.jpg', processed_frame)
            processed_b64 = base64.b64encode(buffer_proc).decode('utf-8')
            
            _, buffer_gray = cv2.imencode('.jpg', gray_scale)
            gray_b64 = base64.b64encode(buffer_gray).decode('utf-8')

            # Prepare the payload to send as JSON
            payload = {
                'box_detected': detected,
                'measurements': measurements,
                'original_image': original_b64,
                'processed_image': processed_b64,
                'gray_scale_image': gray_b64,
                'shape_type': measurements.get('shape', None)
            }
            
            # Send data via HTTP POST request
            requests.post(f"{PC_SERVER_URL}/detector_data", json=payload, timeout=3.0)
            
        except requests.exceptions.RequestException as e:
            styler.print(f"Error sending data to PC: {e}", "error", "red")

    def detection_loop(self):
        """The main detection loop that runs in a separate thread."""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue
            
            detected, processed, measurements, gray_scale = self.detect_black_shapes(frame)
            
            # Use a lock to safely update shared state variables
            with self.lock:
                self.box_detected = detected
                self.detected_shape = measurements.get('shape', None)
                self.box_height = measurements['height']
                self.box_width = measurements['width']
                self.box_area = measurements['area']

            # Send the results to the server
            self.send_to_server(frame, processed, gray_scale, detected, measurements)
            time.sleep(0.5)  # Delay to control the loop rate

    def start_detection(self):
        """Starts the shape detection system in a new thread."""
        if not self.running:
            self.running = True
            self.detection_thread = threading.Thread(target=self.detection_loop)
            self.detection_thread.daemon = True
            self.detection_thread.start()
            styler.print("Shape detection started.", "play", "green")
    
    def stop_detection(self):
        """Stops the shape detection system."""
        if self.running:
            self.running = False
            if self.detection_thread:
                self.detection_thread.join()
            styler.print("Shape detection stopped.", "stop", "yellow")
    
    def cleanup(self):
        """Releases all resources."""
        self.stop_detection()
        if self.cap:
            self.cap.release()
    
    def is_box_present(self):
        """Thread-safe method to check if a box (shape) is detected."""
        with self.lock:
            return self.box_detected
    
    def get_box_measurements(self):
        """Thread-safe method to get the measurements of the detected shape."""
        with self.lock:
            return {
                'height': self.box_height, 
                'width': self.box_width, 
                'area': self.box_area,
                'shape': self.detected_shape
            }
    
    def get_detected_shape(self):
        """Thread-safe method to get the type of detected shape."""
        with self.lock:
            return self.detected_shape

# --- Integration Functions ---
# These functions manage a single, global instance of the BoxDetector.

detector_instance = None

def initialize_box_detector():
    """Initializes and starts the global box detector instance."""
    global detector_instance
    if detector_instance is None:
        styler.print("Initializing geometric shape detector...", "camera", "cyan")
        detector_instance = BoxDetector()
        detector_instance.start_detection()
    return detector_instance

def cleanup_box_detector():
    """Cleans up the resources of the global detector instance."""
    global detector_instance
    if detector_instance:
        detector_instance.cleanup()

def detect_box():
    """Checks if a box (geometric shape) is currently present."""
    global detector_instance
    if detector_instance:
        return detector_instance.is_box_present()
    return False

def get_box_height():
    """Gets the height of the detected box based on its shape."""
    global detector_instance
    if detector_instance:
        measurements = detector_instance.get_box_measurements()
        return measurements['height']
    return 0

def get_detected_shape():
    """Gets the type of shape detected (square, circle, triangle)."""
    global detector_instance
    if detector_instance:
        return detector_instance.get_detected_shape()
    return None

def request_scara_put_routine():
    """Sends a request to the server to make the SCARA robot place a box."""
    try:
        response = requests.post(f"{PC_SERVER_URL}/scara/put_request", timeout=3.0)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        styler.print(f"Error in SCARA PUT request: {e}", "error", "red")
        return False

def request_scara_get_routine():
    """Sends a request to the server to make the SCARA robot retrieve a box."""
    try:
        response = requests.post(f"{PC_SERVER_URL}/scara/get_request", timeout=3.0)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        styler.print(f"Error in SCARA GET request: {e}", "error", "red")
        return False

def is_put_routine_done():
    """Checks the server to see if the SCARA's 'put' routine is finished."""
    try:
        response = requests.get(f"{PC_SERVER_URL}/scara/put_status", timeout=3.0)
        if response.status_code == 200:
            return response.json().get('done', False)
    except requests.exceptions.RequestException:
        return False

def is_get_routine_done():
    """Checks the server to see if the SCARA's 'get' routine is finished."""
    try:
        response = requests.get(f"{PC_SERVER_URL}/scara/get_status", timeout=3.0)
        if response.status_code == 200:
            return response.json().get('done', False)
    except requests.exceptions.RequestException:
        return False

# --- Block for execution as a standalone script ---
if __name__ == "__main__":
    styler.print_title("Geometric Shape Detector - Standalone Test Mode", color="blue")
    
    # Print shape configuration
    styler.print("Shape-to-Height Configuration:", "info", "cyan", bold=True)
    for shape, height in SHAPE_HEIGHTS.items():
        styler.print(f"  {shape.upper()}: {height}cm", "data", "white")
    
    # Initialize the detector
    initialize_box_detector()
    
    def signal_handler(sig, frame):
        """Handles Ctrl+C for a clean shutdown."""
        styler.print("\nShutting down the shape detector...", "bye", "yellow", bold=True)
        cleanup_box_detector()
        sys.exit(0)

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    styler.print("Shape detector is running. Press Ctrl+C to exit.", "info", "white")
    
    # Keep the main script running so the detection thread can work
    while True:
        if detector_instance:
            detected = detector_instance.is_box_present()
            measurements = detector_instance.get_box_measurements()
            shape = measurements.get('shape', 'None')
            height = measurements.get('height', 0)
            
            status_msg = f"Status: {'Shape Detected' if detected else 'No Shape'}"
            if detected:
                status_msg += f" | Shape: {shape.upper()} | Height: {height}cm"
            
            styler.print(status_msg, "debug")
        time.sleep(2)
# box_detector.py
import cv2
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

class BoxDetector:
    """Manages camera operations, detects rectangular boxes, and sends data to a server."""
    
    def __init__(self):
        """Initializes the camera, detection parameters, and state variables."""
        # Camera setup
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            styler.print("Error: Could not open camera.", "error", "red", bold=True)
            sys.exit(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Detection parameters
        self.min_area = 1000  # Minimum contour area to be considered a box.
        self.max_area = 50000  # Maximum contour area.
        self.aspect_ratio_range = (0.5, 2.0)  # Allowed aspect ratio (width/height).
        
        # State variables
        self.box_detected = False
        self.box_height = 0
        self.box_width = 0
        self.box_area = 0
        
        # Threading components
        self.running = False  # Flag to control the detection loop.
        self.detection_thread = None
        self.lock = threading.Lock()  # Lock to ensure thread-safe access to state variables.
        
    def detect_boxes(self, frame):
        """
        Detects rectangular boxes in a given frame.
        
        Args:
            frame: The input image frame from the camera.
            
        Returns:
            A tuple containing:
            - A boolean flag indicating if a box was detected.
            - The processed frame with contours drawn.
            - A dictionary with the box's measurements.
        """
        processed = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        box_detected_flag = False
        measurements = {'height': 0, 'width': 0, 'area': 0}
        
        if contours:
            # Sort contours by area in descending order
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            for contour in contours:
                area = cv2.contourArea(contour)
                if self.min_area < area < self.max_area:
                    # Approximate the contour to a polygon
                    epsilon = 0.02 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)
                    # Check if the polygon has 4 vertices (is a quadrilateral)
                    if len(approx) == 4:
                        (x, y, w, h) = cv2.boundingRect(approx)
                        aspect_ratio = float(w) / h
                        # Check if the aspect ratio is within the desired range
                        if self.aspect_ratio_range[0] <= aspect_ratio <= self.aspect_ratio_range[1]:
                            cv2.drawContours(processed, [approx], -1, (0, 255, 0), 3)
                            box_detected_flag = True
                            measurements = {'height': h, 'width': w, 'area': area}
                            break  # Stop after finding the first valid box
        
        return box_detected_flag, processed, measurements

    def send_to_server(self, original_frame, processed_frame, detected, measurements):
        """
        Encodes images and sends all detection data to the PC server.
        
        Args:
            original_frame: The raw camera frame.
            processed_frame: The frame after processing and drawing contours.
            detected: Boolean indicating if a box was detected.
            measurements: Dictionary of the box's measurements.
        """
        try:
            # Encode images to JPG format and then to base64 strings
            _, buffer_orig = cv2.imencode('.jpg', original_frame)
            original_b64 = base64.b64encode(buffer_orig).decode('utf-8')
            
            _, buffer_proc = cv2.imencode('.jpg', processed_frame)
            processed_b64 = base64.b64encode(buffer_proc).decode('utf-8')
            
            # Prepare the payload to send as JSON
            payload = {
                'box_detected': detected,
                'measurements': measurements,
                'original_image': original_b64,
                'processed_image': processed_b64
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
            
            detected, processed, measurements = self.detect_boxes(frame)
            
            # Use a lock to safely update shared state variables
            with self.lock:
                self.box_detected = detected
                self.box_height = measurements['height']
                self.box_width = measurements['width']
                self.box_area = measurements['area']

            # Send the results to the server
            self.send_to_server(frame, processed, detected, measurements)
            time.sleep(0.5)  # Delay to control the loop rate

    def start_detection(self):
        """Starts the box detection system in a new thread."""
        if not self.running:
            self.running = True
            self.detection_thread = threading.Thread(target=self.detection_loop)
            self.detection_thread.daemon = True  # Allows main program to exit even if thread is running
            self.detection_thread.start()
            styler.print("Box detection started.", "play", "green")
    
    def stop_detection(self):
        """Stops the box detection system."""
        if self.running:
            self.running = False
            if self.detection_thread:
                self.detection_thread.join()  # Wait for the thread to finish
            styler.print("Box detection stopped.", "stop", "yellow")
    
    def cleanup(self):
        """Releases all resources."""
        self.stop_detection()
        if self.cap:
            self.cap.release()
    
    def is_box_present(self):
        """Thread-safe method to check if a box is detected."""
        with self.lock:
            return self.box_detected
    
    def get_box_measurements(self):
        """Thread-safe method to get the measurements of the detected box."""
        with self.lock:
            return {'height': self.box_height, 'width': self.box_width, 'area': self.box_area}

# --- Integration Functions ---
# These functions manage a single, global instance of the BoxDetector.

detector_instance = None

def initialize_box_detector():
    """Initializes and starts the global box detector instance."""
    global detector_instance
    if detector_instance is None:
        styler.print("Initializing box detector...", "camera", "cyan")
        detector_instance = BoxDetector()
        detector_instance.start_detection()
    return detector_instance

def cleanup_box_detector():
    """Cleans up the resources of the global detector instance."""
    global detector_instance
    if detector_instance:
        detector_instance.cleanup()

def detect_box():
    """Checks if a box is currently present."""
    global detector_instance
    if detector_instance:
        return detector_instance.is_box_present()
    return False

def get_box_height():
    """Gets the height of the detected box."""
    global detector_instance
    if detector_instance:
        measurements = detector_instance.get_box_measurements()
        return measurements['height']
    return 0

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
    styler.print_title("Box Detector - Standalone Test Mode", color="blue")
    
    # Initialize the detector
    initialize_box_detector()
    
    def signal_handler(sig, frame):
        """Handles Ctrl+C for a clean shutdown."""
        styler.print("\nShutting down the box detector...", "bye", "yellow", bold=True)
        cleanup_box_detector()
        sys.exit(0)

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    styler.print("Detector is running. Press Ctrl+C to exit.", "info", "white")
    
    # Keep the main script running so the detection thread can work
    while True:
        # You can add status prints here if desired
        if detector_instance:
            detected = detector_instance.is_box_present()
            measurements = detector_instance.get_box_measurements()
            styler.print(f"Status: {'Box Detected' if detected else 'No Box'} | Measurements: {measurements}", "debug")
        time.sleep(2)
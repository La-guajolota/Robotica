#!/home/adrian/py_ros2/bin/python

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from flask import Flask, request, jsonify
import threading
import base64
import numpy as np
import cv2
import json

class RosBridgeServer(Node):
    """
    This node runs a Flask server to communicate with a remote Raspberry Pi.
    """
    def __init__(self):
        super().__init__('ros_bridge_server_node')
        
        # Publishers for captured images and computed data
        self.original_publisher = self.create_publisher(Image, '/box_detector/original_image', 10)
        self.processed_publisher = self.create_publisher(Image, '/box_detector/processed_image', 10)
        self.gray_scale_publisher = self.create_publisher(Image, '/box_detector/gray_scale_image', 10)
        self.detection_publisher = self.create_publisher(Bool, '/box_detector/box_detected', 10)
        self.measurements_publisher = self.create_publisher(String, '/box_detector/measurements', 10)
        
        # Publishers for SCARA requests
        self.scara_put_publisher = self.create_publisher(Bool, '/scara/put_request', 10)
        self.scara_get_publisher = self.create_publisher(Bool, '/scara/get_request', 10)
        
        # Subscribers for SCARA responses
        self.create_subscription(Bool, '/scara/put_response', self.scara_put_callback, 10)
        self.create_subscription(Bool, '/scara/get_response', self.scara_get_callback, 10)
        
        # Utilities and state flags
        self.cv_bridge = CvBridge()
        self.put_routine_done = False
        self.get_routine_done = False
        
        self.get_logger().info('ROS2 Bridge Server initialized.')

    # SCARA Callbacks
    def scara_put_callback(self, msg):
        self.put_routine_done = msg.data
        if msg.data:
            self.get_logger().info('Response received: SCARA PUT routine completed.')
    
    def scara_get_callback(self, msg):
        self.get_routine_done = msg.data
        if msg.data:
            self.get_logger().info('Response received: SCARA GET routine completed.')
            
    # Function to publish data to ROS2 topics
    def publish_detector_data(self, data):
        try:
            # Publish detection state
            detection_msg = Bool()
            detection_msg.data = data['box_detected']
            self.detection_publisher.publish(detection_msg)
            
            # Publish measurements
            measurements_msg = String()
            measurements_msg.data = json.dumps(data['measurements'])
            self.measurements_publisher.publish(measurements_msg)
            
            # Decode and publish original image
            img_bytes = base64.b64decode(data['original_image'])
            np_arr = np.frombuffer(img_bytes, np.uint8)
            cv_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            self.original_publisher.publish(self.cv_bridge.cv2_to_imgmsg(cv_img, "bgr8"))

            # Decode and publish processed image
            img_bytes_proc = base64.b64decode(data['processed_image'])
            np_arr_proc = np.frombuffer(img_bytes_proc, np.uint8)
            cv_img_proc = cv2.imdecode(np_arr_proc, cv2.IMREAD_COLOR)
            self.processed_publisher.publish(self.cv_bridge.cv2_to_imgmsg(cv_img_proc, "bgr8"))

            # Decode and publish gray scale image
            img_bytes_gray = base64.b64decode(data['gray_scale_image'])
            np_arr_gray = np.frombuffer(img_bytes_gray, np.uint8)
            cv_img_gray = cv2.imdecode(np_arr_gray, cv2.IMREAD_GRAYSCALE)
            self.gray_scale_publisher.publish(self.cv_bridge.cv2_to_imgmsg(cv_img_gray, "mono8"))
            
        except Exception as e:
            self.get_logger().error(f"Error publishing detector data: {e}")

    def request_scara_put(self):
        msg = Bool()
        msg.data = True
        self.scara_put_publisher.publish(msg)
        self.put_routine_done = False  # Reset state
        self.get_logger().info('PUT request sent to SCARA.')
        
    def request_scara_get(self):
        msg = Bool()
        msg.data = True
        self.scara_get_publisher.publish(msg)
        self.get_routine_done = False  # Reset state
        self.get_logger().info('GET request sent to SCARA.')

# --- Flask Configuration ---
app = Flask(__name__)
ros_node = None

@app.route('/detector_data', methods=['POST'])
def handle_detector_data():
    if ros_node:
        data = request.json
        ros_node.publish_detector_data(data)
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "error", "message": "ROS node not ready"}), 500

@app.route('/scara/put_request', methods=['POST'])
def handle_scara_put():
    if ros_node:
        ros_node.request_scara_put()
        return jsonify({"status": "request sent"}), 200
    return jsonify({"status": "error", "message": "ROS node not ready"}), 500

@app.route('/scara/get_request', methods=['POST'])
def handle_scara_get():
    if ros_node:
        ros_node.request_scara_get()
        return jsonify({"status": "request sent"}), 200
    return jsonify({"status": "error", "message": "ROS node not ready"}), 500

@app.route('/scara/put_status', methods=['GET'])
def get_put_status():
    if ros_node:
        done = ros_node.put_routine_done
        if done:
            ros_node.put_routine_done = False  # Reset after checking
        return jsonify({"done": done}), 200
    return jsonify({"status": "error", "message": "ROS node not ready"}), 500

@app.route('/scara/get_status', methods=['GET'])
def get_get_status():
    if ros_node:
        done = ros_node.get_routine_done
        if done:
            ros_node.get_routine_done = False  # Reset after checking
        return jsonify({"done": done}), 200
    return jsonify({"status": "error", "message": "ROS node not ready"}), 500

def run_flask_app():
    # Run Flask in production mode with a WSGI server like waitress or gunicorn
    app.run(host='0.0.0.0', port=5001, debug=False)

def main(args=None):
    global ros_node
    rclpy.init(args=args)
    ros_node = RosBridgeServer()
    
    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Keep the ROS node spinning in the main thread
    try:
        rclpy.spin(ros_node)
    except KeyboardInterrupt:
        pass
    finally:
        ros_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

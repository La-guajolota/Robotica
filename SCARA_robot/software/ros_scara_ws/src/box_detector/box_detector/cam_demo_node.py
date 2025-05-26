# box_detector/box_detector/cam_demo_node.py

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CamDemoNode(Node):
    def __init__(self):
        super().__init__('cam_demo_node')

        # Declarar parámetro de cámara
        self.declare_parameter('cam_index', 0)
        cam_index = self.get_parameter('cam_index').get_parameter_value().integer_value
        self.get_logger().info(f"Usando cámara con índice: {cam_index}")

        self.image_pub = self.create_publisher(Image, 'processed_image', 10)
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(cam_index)

        if not self.cap.isOpened():
            self.get_logger().error(f"No se pudo abrir la cámara con índice {cam_index}")
        else:
            self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn('Failed to grab frame')
            return

        processed_frame = self.detect_boxes(frame)
        ros_image = self.bridge.cv2_to_imgmsg(processed_frame, encoding="bgr8")
        self.image_pub.publish(ros_image)
        cv2.waitKey(1)

    def detect_boxes(self, frame):
        # TODO: Detection logic
        return frame

    def destroy_node(self):
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CamDemoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

#!/home/adrian/py_ros2/bin/python

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import argparse

class CamDemoNode(Node):
    def __init__(self, cam_index):
        super().__init__('cam_demo_node')

        # Inicializar la cámara con el índice proporcionado
        self.get_logger().info(f"Usando cámara con índice: {cam_index}")
        self.cap = cv2.VideoCapture(cam_index)

        if not self.cap.isOpened():
            self.get_logger().error(f"No se pudo abrir la cámara con índice {cam_index}")
            raise RuntimeError(f"No se pudo abrir la cámara con índice {cam_index}")

        # Publicador de imágenes procesadas
        self.image_pub = self.create_publisher(Image, 'processed_image', 10)
        self.bridge = CvBridge()

        # Crear un temporizador para procesar frames periódicamente
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn('Failed to grab frame')
            return

        # Procesar el frame para detectar objetos y medir dimensiones
        processed_frame = self.process_frame(frame)
        ros_image = self.bridge.cv2_to_imgmsg(processed_frame, encoding="bgr8")
        self.image_pub.publish(ros_image)

    def process_frame(self, frame):
        """
        Procesa el frame para detectar objetos y medir dimensiones utilizando el canal Cb del espacio de color YCrCb.
        """
        # Convertir la imagen al espacio de color YCrCb y extraer el canal Cb
        ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        _, _, cb = cv2.split(ycrcb)

        # Aplicar un desenfoque gaussiano al canal Cb
        blurred = cv2.GaussianBlur(cb, (7, 7), 0)

        # Detección de bordes utilizando Canny
        edged = cv2.Canny(blurred, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        # Encontrar contornos
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts, _ = contours.sort_contours(cnts)

        # Procesar contornos
        try:
            orig, box = self.measure_obj(cnts, frame)
            orig = self.draw_objs(orig, box)
        except TypeError:
            # Si no se encuentra un contorno válido, devolver el frame original
            orig = frame

        return orig

    def measure_obj(self, cnts, image):
        """
        Mide las dimensiones de los objetos en la imagen basándose en los contornos.
        """
        for c in cnts:
            # Ignorar contornos pequeños
            if cv2.contourArea(c) < 100:
                continue

            # Calcular el cuadro delimitador rotado del contorno
            orig = image.copy()
            box = cv2.minAreaRect(c)
            box = cv2.boxPoints(box) if not imutils.is_cv2() else cv2.cv.BoxPoints(box)
            box = np.array(box, dtype="int")

            # Ordenar los puntos y dibujar el cuadro delimitador
            box = perspective.order_points(box)
            return orig, box

    def draw_objs(self, orig, box, pixelsPerMetric=None):
        """
        Dibuja el cuadro delimitador, puntos medios y dimensiones del objeto.
        """
        # Desempaquetar los puntos del cuadro delimitador
        (tl, tr, br, bl) = box

        # Calcular puntos medios
        (tltrX, tltrY) = self.midpoint(tl, tr)
        (blbrX, blbrY) = self.midpoint(bl, br)
        (tlblX, tlblY) = self.midpoint(tl, bl)
        (trbrX, trbrY) = self.midpoint(tr, br)

        # Calcular distancias
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        # Calibrar píxeles por métrica si no se proporciona
        if pixelsPerMetric is None:
            pixelsPerMetric = dB / 10  # Ejemplo: 10 unidades como referencia

        # Calcular dimensiones del objeto
        dimA = dA / pixelsPerMetric
        dimB = dB / pixelsPerMetric

        # Dibujar dimensiones en la imagen
        cv2.putText(orig, "{:.1f}in".format(dimA), (int(tltrX - 15), int(tltrY - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        cv2.putText(orig, "{:.1f}in".format(dimB), (int(trbrX + 10), int(trbrY)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        return orig

    def midpoint(self, ptA, ptB):
        """
        Calcula el punto medio entre dos puntos.
        """
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

    def destroy_node(self):
        if self.cap.isOpened():
            self.cap.release()
        super().destroy_node()


def main(args=None):
    # Parsear argumentos de línea de comandos para seleccionar la cámara
    parser = argparse.ArgumentParser(description='Nodo de detección de objetos con ROS 2.')
    parser.add_argument('--cam_index', type=int, default=0, help='Índice de la cámara a usar (por defecto: 0)')
    args = parser.parse_args()

    rclpy.init(args=None)
    try:
        node = CamDemoNode(cam_index=args.cam_index)
        rclpy.spin(node)
    except RuntimeError as e:
        print(f"Error: {e}")
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()

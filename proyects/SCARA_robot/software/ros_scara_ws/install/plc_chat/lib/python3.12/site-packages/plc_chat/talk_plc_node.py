import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Int32MultiArray
import snap7
from snap7.util import *
import time

# Definir áreas manualmente
class Areas:
    MK = 0x83  # Área de memoria de marcas

# Crear cliente PLC
plc = snap7.client.Client()

def connect_to_plc(ip_address):
    """Conecta al PLC usando la dirección IP proporcionada."""
    try:
        plc.connect(ip_address, 0, 1)  # ip, rack, slot
        print(f"Conectado al PLC en {ip_address}")
    except Exception as e:
        print(f"Error al conectar al PLC: {e}")

def disconnect_from_plc():
    """Desconecta del PLC."""
    try:
        plc.disconnect()
        print("Desconectado del PLC")
    except Exception as e:
        print(f"Error al desconectar del PLC: {e}")

def read_marca(byte_index, start_byte):
    """Lee un byte de la memoria de marcas."""
    try:
        data = plc.read_area(Areas.MK, 0, byte_index, 1)
        return get_byte(data, start_byte)
    except Exception as e:
        print(f"Error al leer marcas: {e}")
        return None

def write_m_bit(byte_index, bit_index, value):
    """Escribe un bit en la memoria de marcas."""
    try:
        # Leer el byte actual de la memoria de marcas
        data = plc.read_area(Areas.MK, 0, byte_index, 1)
        # Modificar el bit específico
        set_bool(data, 0, bit_index, value)
        # Escribir el byte modificado de vuelta en la memoria de marcas
        plc.write_area(Areas.MK, 0, byte_index, data)
        print(f"Bit M{byte_index}.{bit_index} establecido en {value}")
    except Exception as e:
        print(f"Error al escribir bit: {e}")

def write_dimensions(byte_index, width, height):
    """Escribe las dimensiones de la caja (ancho y alto) en la memoria de marcas."""
    try:
        # Crear un buffer para las dimensiones
        data = bytearray(4)
        set_int(data, 0, width)  # Escribir ancho (2 bytes)
        set_int(data, 2, height)  # Escribir alto (2 bytes)
        # Escribir el buffer en la memoria de marcas
        plc.write_area(Areas.MK, 0, byte_index, data)
        print(f"Dimensiones escritas en M{byte_index}: Ancho={width}, Alto={height}")
    except Exception as e:
        print(f"Error al escribir dimensiones: {e}")

class TalkPLCNode(Node):
    def __init__(self):
        super().__init__('talk_plc_node')

        # Declarar parámetros
        self.declare_parameter('plc_ip', '192.168.0.1')  # Cambiar por la IP del PLC
        self.plc_ip = self.get_parameter('plc_ip').get_parameter_value().string_value

        # Conectar al PLC
        connect_to_plc(self.plc_ip)

        # Suscriptor para recibir comandos de ROS 2
        self.subscription = self.create_subscription(
            Int32MultiArray,
            'plc_dimensions',
            self.dimensions_callback,
            10
        )

        # Publicador para enviar el estado del PLC
        self.publisher = self.create_publisher(Bool, 'plc_status', 10)

        # Crear un temporizador para leer datos periódicamente
        self.timer = self.create_timer(1.0, self.read_plc_status)

    def dimensions_callback(self, msg):
        """
        Callback para recibir dimensiones desde un tópico de ROS 2.
        """
        try:
            width, height = msg.data
            write_dimensions(1, width, height)  # Escribir dimensiones en el PLC
            self.get_logger().info(f"Dimensiones recibidas: Ancho={width}, Alto={height}")
        except Exception as e:
            self.get_logger().error(f"Error al procesar dimensiones: {e}")

    def read_plc_status(self):
        """
        Lee el estado del PLC y lo publica en un tópico.
        """
        try:
            hay_caja = read_marca(0, 0)  # Leer si hay caja (M0.0)
            msg = Bool()
            msg.data = bool(hay_caja)
            self.publisher.publish(msg)
            self.get_logger().info(f"Estado del PLC publicado: Hay caja={msg.data}")
        except Exception as e:
            self.get_logger().error(f"Error al leer estado del PLC: {e}")

    def destroy_node(self):
        """
        Sobrescribe el método destroy_node para desconectar del PLC.
        """
        disconnect_from_plc()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = TalkPLCNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

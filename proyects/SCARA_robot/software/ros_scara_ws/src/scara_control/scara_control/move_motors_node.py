#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_msg_svrs.srv import MotorControl  # Importamos el nuevo servicio
import argparse  # Importamos argparse para manejar argumentos de línea de comandos

class MotorControlClient(Node):
    def __init__(self):
        super().__init__('Motors_control')

        # Cliente para el nuevo servicio MotorControl
        self.cli = self.create_client(MotorControl, 'move_X_motor')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        self.req = MotorControl.Request()

    def send_request(self, data_uint8, data_bool, data_float):
        # Asignamos los valores a los campos del servicio
        self.req.data_uint8 = data_uint8
        self.req.data_bool = data_bool
        self.req.data_float = data_float
        return self.cli.call_async(self.req)

def str_to_bool(value):
    """Convierte una cadena en un valor booleano."""
    if value.lower() in ('true', '1', 'yes'):
        return True
    elif value.lower() in ('false', '0', 'no'):
        return False
    else:
        raise argparse.ArgumentTypeError(f"Boolean value expected, got '{value}'.")

def main(args=None):
    # Parseamos los argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Control SCARA motor via ROS2 service.')
    parser.add_argument('data_uint8', type=int, help='Unsigned integer value to send to the motor (0-255)')
    parser.add_argument('data_bool', type=str_to_bool, help='Boolean value to send to the motor (true/false)')
    parser.add_argument('data_float', type=float, help='Float value to send to the motor (e.g., 270.0)')
    parsed_args = parser.parse_args()

    # Inicializamos rclpy con los argumentos de línea de comandos
    rclpy.init(args=None)

    motors_control_client = MotorControlClient()
    future = motors_control_client.send_request(
        parsed_args.data_uint8, 
        parsed_args.data_bool, 
        parsed_args.data_float
    )

    rclpy.spin_until_future_complete(motors_control_client, future)
    
    response = future.result()
    if response is not None:
        motors_control_client.get_logger().info('Response: %s' % (response.response_message))
    else:
        motors_control_client.get_logger().error('Service call failed.')

    motors_control_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import time
from collections import deque
import argparse

class ReadEncodersSubscriber(Node):
    
    def __init__(self):
        super().__init__('Encoders')
        
        # Inicializar los valores de los encoders
        self.encoder_a_value = 0.0
        self.encoder_b_value = 0.0
        self.encoder_c_value = 0.0

        # Buffers para el promedio móvil
        self.moving_avg_window_size = 3
        self.encoder_a_buffer = deque(maxlen=self.moving_avg_window_size)
        self.encoder_b_buffer = deque(maxlen=self.moving_avg_window_size)
        self.encoder_c_buffer = deque(maxlen=self.moving_avg_window_size)
        
        # Suscripción al encoder A
        self.subscription_a = self.create_subscription(
            Float32,
            'encoderA_angle_pub',
            self.listener_callback_a,
            10)
        
        # Suscripción al encoder B
        self.subscription_b = self.create_subscription(
            Float32,
            'encoderB_angle_pub',
            self.listener_callback_b,
            10)
        
        # Suscripción al encoder C
        self.subscription_c = self.create_subscription(
            Float32,
            'encoderC_angle_pub',
            self.listener_callback_c,
            10)
    
    def print_all_encoders(self):
        output = ('LINK1: {:6.2f}° | LINK2: {:6.2f}° | BASE: {:6.2f}°'.format(
                    self.encoder_a_value, self.encoder_b_value, self.encoder_c_value))
        print('\r' + output, end='')  # Sobrescribir la línea en la terminal

    def apply_low_pass_filter(self, current_value, buffer):
        buffer.append(current_value)
        return sum(buffer) / len(buffer)  # Promedio móvil simple

    def listener_callback_a(self, msg):
        raw_value = round(msg.data, 2)
        filtered_value = self.apply_low_pass_filter(raw_value, self.encoder_a_buffer)
        self.encoder_a_value = filtered_value
        self.print_all_encoders()
    
    def listener_callback_b(self, msg):
        raw_value = round(msg.data, 2)
        filtered_value = self.apply_low_pass_filter(raw_value, self.encoder_b_buffer)
        self.encoder_b_value = filtered_value
        self.print_all_encoders()
    
    def listener_callback_c(self, msg):
        raw_value = round(msg.data, 2)
        filtered_value = self.apply_low_pass_filter(raw_value, self.encoder_c_buffer)
        self.encoder_c_value = filtered_value
        self.print_all_encoders()

def main(args=None):
    rclpy.init(args=None)
    
    encoders_subscriber = ReadEncodersSubscriber()
    
    rclpy.spin(encoders_subscriber)
    
    # Destroy the node explicitly
    encoders_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

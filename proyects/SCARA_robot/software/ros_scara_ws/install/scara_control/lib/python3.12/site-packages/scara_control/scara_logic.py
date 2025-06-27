#!/home/adrian/py_ros2/bin/python

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from custom_msg_svrs.srv import MotorControl
import time

class ScaraLogicNode(Node):
    def __init__(self):
        super().__init__('scara_logic_node')
        
        # Cliente para el servicio de control de motores
        self.motor_client = self.create_client(MotorControl, 'move_X_motor')
        while not self.motor_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Motor control service not available, waiting again...')
        
        # Subscribers para recibir las órdenes
        self.put_subscriber = self.create_subscription(
            Bool,
            '/scara/put_request',
            self.put_request_callback,
            10)
        
        self.get_subscriber = self.create_subscription(
            Bool,
            '/scara/get_request',
            self.get_request_callback,
            10)
        
        # Subscriber para el end_of_service
        self.end_of_service_subscriber = self.create_subscription(
            Bool,
            '/end_of_service_pub',
            self.end_of_service_callback,
            10)
        
        # Publishers para enviar las respuestas
        self.put_response_publisher = self.create_publisher(Bool, '/scara/put_response', 10)
        self.get_response_publisher = self.create_publisher(Bool, '/scara/get_response', 10)
        
        # Estado del servicio
        self.service_completed = False
        self.waiting_for_service_completion = False
        
        self.get_logger().info('SCARA Logic Node initialized and ready.')

    def end_of_service_callback(self, msg):
        """
        Callback para el topic end_of_service_pub
        """
        if msg.data and self.waiting_for_service_completion:
            self.service_completed = True
            self.waiting_for_service_completion = False
            self.get_logger().info('Service movement completed, ready for next command')

    def send_motor_command_and_wait(self, motor_id, direction, angle):
        """
        Envía un comando al servicio de control de motores y espera a que termine
        """
        # Resetear estado
        self.service_completed = False
        self.waiting_for_service_completion = False
        
        # Enviar comando
        req = MotorControl.Request()
        req.data_uint8 = motor_id      # ID del motor (0-255)
        req.data_bool = direction      # Dirección del motor (True/False)
        req.data_float = angle         # Ángulo a mover (grados)
        
        future = self.motor_client.call_async(req)
        
        # Esperar respuesta del servicio (confirmación de recepción)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        
        if response is None:
            self.get_logger().error('Motor service call failed.')
            return False
        
        self.get_logger().info(f'Motor command sent: {response.response_message}')
        
        # Ahora esperar a que el movimiento termine
        self.waiting_for_service_completion = True
        self.get_logger().info(f'Waiting for movement completion (Motor {motor_id}, Angle: {angle}°)...')
        
        # Esperar hasta que end_of_service_pub publique True
        timeout_counter = 0
        max_timeout = 100  # 10 segundos (100 * 0.1s)
        
        while not self.service_completed and timeout_counter < max_timeout:
            rclpy.spin_once(self, timeout_sec=0.1)
            timeout_counter += 1
        
        if self.service_completed:
            self.get_logger().info('Movement completed successfully')
            return True
        else:
            self.get_logger().error('Timeout waiting for movement completion')
            self.waiting_for_service_completion = False
            return False

    def execute_put_routine(self):
        """
        Ejecuta la rutina PUT del SCARA
        Ejemplo de secuencia de movimientos para colocar un objeto
        """
        self.get_logger().info('Starting PUT routine...')
        
        try:
            # Paso 1: Mover base a posición inicial
            self.get_logger().info('Step 1: Moving base to initial position')
            #if not self.send_motor_command_and_wait(motor_id=3, direction=True, angle=0.0):
            #    return False
            
            # Paso 2: Mover link1 a posición de aproximación
            self.get_logger().info('Step 2: Moving link1 to approach position')
            #if not self.send_motor_command_and_wait(motor_id=1, direction=True, angle=45.0):
            #    return False
            
            # Paso 3: Mover link2 para extender el brazo
            self.get_logger().info('Step 3: Extending arm with link2')
            #if not self.send_motor_command_and_wait(motor_id=2, direction=True, angle=90.0):
            #    return False
            
            # Paso 4: Bajar para colocar objeto
            self.get_logger().info('Step 4: Lowering to place object')
            #if not self.send_motor_command_and_wait(motor_id=2, direction=False, angle=120.0):
            #    return False
            
            # Paso 5: Retraer brazo
            self.get_logger().info('Step 5: Retracting arm')
            #if not self.send_motor_command_and_wait(motor_id=2, direction=True, angle=45.0):
            #    return False
            
            # Paso 6: Regresar a posición home
            self.get_logger().info('Step 6: Returning to home position')
            #if not self.send_motor_command_and_wait(motor_id=1, direction=False, angle=0.0):
            #    return False
            
            self.get_logger().info('PUT routine completed successfully!')
            return True
            
        except Exception as e:
            self.get_logger().error(f'Error in PUT routine: {str(e)}')
            return False

    def execute_get_routine(self):
        """
        Ejecuta la rutina GET del SCARA
        Ejemplo de secuencia de movimientos para tomar un objeto
        """
        self.get_logger().info('Starting GET routine...')
        
        try:
            # Paso 1: Mover base a posición de objeto
            self.get_logger().info('Step 1: Moving base to object position')
            #if not self.send_motor_command_and_wait(motor_id=3, direction=True, angle=90.0):
            #    return False
            
            # Paso 2: Posicionar link1 para aproximación
            self.get_logger().info('Step 2: Positioning link1 for approach')
            #if not self.send_motor_command_and_wait(motor_id=1, direction=True, angle=30.0):
            #    return False
            
            # Paso 3: Extender brazo hacia objeto
            self.get_logger().info('Step 3: Extending arm towards object')
            #if not self.send_motor_command_and_wait(motor_id=2, direction=True, angle=135.0):
            #    return False
            
            # Paso 4: Bajar para tomar objeto
            self.get_logger().info('Step 4: Lowering to pick up object')
            #if not self.send_motor_command_and_wait(motor_id=2, direction=True, angle=150.0):
            #    return False
            
            # Paso 5: Levantar con objeto
            self.get_logger().info('Step 5: Lifting with object')
            #if not self.send_motor_command_and_wait(motor_id=2, direction=False, angle=90.0):
            #    return False
            
            # Paso 6: Mover a posición de entrega
            self.get_logger().info('Step 6: Moving to delivery position')
            #if not self.send_motor_command_and_wait(motor_id=3, direction=False, angle=180.0):
            #    return False
            
            # Paso 7: Regresar a home
            self.get_logger().info('Step 7: Returning to home position')
            #if not self.send_motor_command_and_wait(motor_id=1, direction=False, angle=0.0):
            #    return False
            
            #if not self.send_motor_command_and_wait(motor_id=3, direction=False, angle=0.0):
            #    return False
            
            self.get_logger().info('GET routine completed successfully!')
            return True
            
        except Exception as e:
            self.get_logger().error(f'Error in GET routine: {str(e)}')
            return False

    def put_request_callback(self, msg):
        """
        Callback para manejar requests PUT
        """
        if msg.data:
            self.get_logger().info('Received PUT request')
            success = self.execute_put_routine()
            
            # Enviar respuesta
            response_msg = Bool()
            response_msg.data = success
            self.put_response_publisher.publish(response_msg)
            
            if success:
                self.get_logger().info('PUT routine completed and response sent')
            else:
                self.get_logger().error('PUT routine failed')

    def get_request_callback(self, msg):
        """
        Callback para manejar requests GET
        """
        if msg.data:
            self.get_logger().info('Received GET request')
            success = self.execute_get_routine()
            
            # Enviar respuesta
            response_msg = Bool()
            response_msg.data = success
            self.get_response_publisher.publish(response_msg)
            
            if success:
                self.get_logger().info('GET routine completed and response sent')
            else:
                self.get_logger().error('GET routine failed')

def main(args=None):
    rclpy.init(args=args)
    
    scara_logic_node = ScaraLogicNode()
    
    try:
        rclpy.spin(scara_logic_node)
    except KeyboardInterrupt:
        pass
    finally:
        scara_logic_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
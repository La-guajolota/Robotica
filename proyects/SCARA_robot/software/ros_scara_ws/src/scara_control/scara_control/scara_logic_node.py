#!/home/adrian/py_ros2/bin/python

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from custom_msg_svrs.srv import MotorControl

class ScaraLogicNode(Node):
    def __init__(self):
        super().__init__('scara_logic_node')
        
        # Cliente para el servicio de control de motores
        self.motor_client = self.create_client(MotorControl, 'move_X_motor')
        while not self.motor_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Motor control service not available, waiting again...')
        
        # Subscribers
        self.put_subscriber = self.create_subscription(
            Bool, '/scara/put_request', self.put_request_callback, 10)
        
        self.get_subscriber = self.create_subscription(
            Bool, '/scara/get_request', self.get_request_callback, 10)
        
        self.end_of_service_subscriber = self.create_subscription(
            Bool, 'end_of_service_pub', self.end_of_service_callback, 10)
        
        # Publishers
        self.put_response_publisher = self.create_publisher(Bool, '/scara/put_response', 10)
        self.get_response_publisher = self.create_publisher(Bool, '/scara/get_response', 10)
        
        # Estado simple
        self.can_proceed = True  # True cuando end_of_service_pub envía True
        self.current_routine = None  # 'put' o 'get'
        self.routine_steps = []
        self.current_step = 0
        
        self.get_logger().info('SCARA Logic Node initialized and ready.')

    def end_of_service_callback(self, msg):
        """Cuando recibe True, puede proceder al siguiente paso"""
        if msg.data is True:
            self.can_proceed = True
            self.get_logger().info('✅ Service completed - can proceed to next step')
            self.execute_next_step()
        else:
            self.can_proceed = False
            self.get_logger().info('🔄 Service started - waiting...')

    def send_motor_command(self, motor_id, direction, angle):
        """Envía comando al motor sin esperar"""
        req = MotorControl.Request()
        req.data_uint8 = motor_id
        req.data_bool = direction
        req.data_float = angle
        
        self.can_proceed = False  # Bloqueamos hasta recibir confirmación
        future = self.motor_client.call_async(req)
        self.get_logger().info(f'Sent: Motor {motor_id}, {"CW" if direction else "CCW"}, {angle}°')

    def execute_next_step(self):
        """Ejecuta el siguiente paso de la rutina actual"""
        if not self.current_routine or not self.can_proceed:
            return
            
        if self.current_step < len(self.routine_steps):
            step = self.routine_steps[self.current_step]
            self.get_logger().info(f'Executing step {self.current_step + 1}/{len(self.routine_steps)}: {step["name"]}')
            
            self.send_motor_command(step['motor'], step['direction'], step['angle'])
            self.current_step += 1
        else:
            # Rutina completada
            self.finish_routine(success=True)

    def finish_routine(self, success):
        """Finaliza la rutina actual y envía respuesta"""
        routine_type = self.current_routine
        self.current_routine = None
        self.routine_steps = []
        self.current_step = 0
        
        response_msg = Bool()
        response_msg.data = success
        
        if routine_type == 'put':
            self.put_response_publisher.publish(response_msg)
            self.get_logger().info(f'>>> PUT routine finished ({("SUCCESS" if success else "FAILURE")}) <<<')
        elif routine_type == 'get':
            self.get_response_publisher.publish(response_msg)
            self.get_logger().info(f'>>> GET routine finished ({("SUCCESS" if success else "FAILURE")}) <<<')

    def put_request_callback(self, msg):
        """Inicia rutina PUT"""
        if msg.data and not self.current_routine:
            self.get_logger().info('>>> Starting PUT routine <<<')
            self.current_routine = 'put'
            self.current_step = 0
            
            # Define los pasos de la rutina PUT
            self.routine_steps = [
                {'name': 'Close gripper', 'motor': 4, 'direction': False, 'angle': 0.0},
                {'name': 'Test movement', 'motor': 0, 'direction': True, 'angle': 3600.0},
                {'name': 'Open gripper', 'motor': 4, 'direction': True, 'angle': 0.0},
                {'name': 'Test movement', 'motor': 0, 'direction': False, 'angle': 3600.0},
            ]
            
            # Inicia la rutina si puede proceder
            if self.can_proceed:
                self.execute_next_step()
                

    def get_request_callback(self, msg):
        """Inicia rutina GET"""
        if msg.data and not self.current_routine:
            self.get_logger().info('>>> Starting GET routine <<<')
            self.current_routine = 'get'
            self.current_step = 0
            
            # Define los pasos de la rutina GET
            self.routine_steps = [
                {'name': 'Test movement', 'motor': 0, 'direction': True, 'angle': 3600.0},
                {'name': 'Test movement', 'motor': 0, 'direction': False, 'angle': 3600.0},
                {'name': 'Close gripper', 'motor': 4, 'direction': False, 'angle': 0.0},
                {'name': 'Open gripper', 'motor': 4, 'direction': True, 'angle': 0.0}

            ]
            
            # Inicia la rutina si puede proceder
            if self.can_proceed:
                self.execute_next_step()

def main(args=None):
    rclpy.init(args=args)
    scara_logic_node = ScaraLogicNode()
    
    try:
        rclpy.spin(scara_logic_node)
    except KeyboardInterrupt:
        scara_logic_node.get_logger().info('Node stopped cleanly.')
    finally:
        scara_logic_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
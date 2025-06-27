/**
 * @file microros_utils.h
 * @brief MicroROS utilities for SCARA robot communication
 * @author Adrián Silva Palafox
 * @date Apr 2025
 */

 #ifndef MICROROS_UTILS_H
 #define MICROROS_UTILS_H
 
 #ifdef __cplusplus
 extern "C" {
 #endif
 
 #include <Arduino.h>
 
 // MicroROS includes
 #include <rcl/rcl.h>
 #include <rcl/service.h>
 #include <rclc/rclc.h>
 #include <rclc/executor.h>
 #include <rosidl_runtime_c/string_functions.h>
 
 // ROS message types
 #include <std_msgs/msg/float32.h>
 #include <std_msgs/msg/u_int8.h>
 #include <std_msgs/msg/bool.h>
 #include <std_srvs/srv/set_bool.h>
 #include <custom_msg_svrs/srv/motor_control.h>
 
 /**
  * @brief Error checking macros for ROS functions
  */
 #define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
 #define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}
 
 /**
  * @section PUBLISHERS
  * ROS Publishers for encoder angle data
  */
 
 // Encoder publishers - DECLARACIÓN EXTERNA
 extern rcl_publisher_t encoderA_pub;
 extern std_msgs__msg__Float32 encoderA_angle_msg;
 
 extern rcl_publisher_t encoderB_pub;
 extern std_msgs__msg__Float32 encoderB_angle_msg;
 
 extern rcl_publisher_t encoderC_pub;
 extern std_msgs__msg__Float32 encoderC_angle_msg;

 // End of service 
 extern rcl_publisher_t end_of_service_pub;
 extern std_msgs__msg__Bool end_of_service_msg; 
 
 /**
  * @section SERVICES
  * ROS Service definitions for motor control
  */
 
 // Service flags and parameters
 extern volatile uint16_t services_flags;
 extern volatile bool dir[3];             
 extern volatile float angle[3];          
 extern volatile bool tool_servo;         
 
 // Service flag bit definitions
 #define MOVE_BASE_SERVICE   0x01   // Bit 0
 #define MOVE_LINK1_SERVICE  0x02   // Bit 1
 #define MOVE_LINK2_SERVICE  0x04   // Bit 2
 #define TOOL_SERVICE        0x08   // Bit 3
 
 // Motor control service components - DECLARACIÓN EXTERNA
 extern rcl_service_t move_motor_server;
 extern rmw_request_id_t header_response;
 extern custom_msg_svrs__srv__MotorControl_Request srv_req;
 extern custom_msg_svrs__srv__MotorControl_Response srv_res;
 
//  // Tool control service - CORREGIDO EL TIPO DE RESPUESTA
//  extern rcl_service_t tool_control_server;
//  extern std_srvs__srv__SetBool_Request tool_control_req;
//  extern std_srvs__srv__SetBool_Response tool_control_res;  // CORREGIDO: era Request, debe ser Response
 
 /**
  * @section ROS_COMPONENTS
  * Core MicroROS components - DECLARACIÓN EXTERNA
  */
 extern rclc_executor_t executor;
 extern rclc_support_t support;
 extern rcl_allocator_t allocator;
 extern rcl_node_t node;
 extern rcl_timer_t timer;
 
 /**
  * @section FUNCTIONS
  * MicroROS utility functions
  */
 
 void error_loop();
 void timer_publisher_encoders(rcl_timer_t * timer, int64_t last_call_time);
 void publish_encoder_values(void);
 void service_server_movemotor(const void * request_msg, void * response_msg);
 //void service_server_toolcontrol(const void * request_msg, void * response_msg);
 void publish_end_of_service(bool status);
 void setup_micro_ros_scara(void);

 
 // --- NUEVA FUNCIÓN DE DEBUG ---
// Declara una función simple para imprimir mensajes que será visible para los archivos C.
void print_debug(const char *msg);

 #ifdef __cplusplus
 }
 #endif
 
 #endif // MICROROS_UTILS_H
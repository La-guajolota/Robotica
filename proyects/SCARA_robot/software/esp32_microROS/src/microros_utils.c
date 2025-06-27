/**
 * @file microros_utils.c
 * @brief Implementation of MicroROS utilities for SCARA robot communication
 * @author Adrián Silva Palafox
 * @date Apr 2025
 */

#include "microros_utils.h"

/**
 * @section GLOBAL_VARIABLES
 * Definición de todas las variables globales
 */

// ROS Components
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

// Publishers of encoders
rcl_publisher_t encoderA_pub;
std_msgs__msg__Float32 encoderA_angle_msg;

rcl_publisher_t encoderB_pub;
std_msgs__msg__Float32 encoderB_angle_msg;

rcl_publisher_t encoderC_pub;
std_msgs__msg__Float32 encoderC_angle_msg;

// Publisher of end of service
rcl_publisher_t end_of_service_pub;
std_msgs__msg__Bool end_of_service_msg;

// Service variables
volatile uint16_t services_flags = 0x00;
volatile bool dir[3] = {0};
volatile float angle[3] = {0};
volatile bool tool_servo = false;

// Motor control service
rcl_service_t move_motor_server;
rmw_request_id_t header_response;
custom_msg_svrs__srv__MotorControl_Request srv_req;
custom_msg_svrs__srv__MotorControl_Response srv_res;

// Tool control service
// rcl_service_t tool_control_server;
// std_srvs__srv__SetBool_Request tool_control_req;
// std_srvs__srv__SetBool_Response tool_control_res;

/**
 * @brief Error handling loop
 */
void error_loop() {
    while(1) {
        delay(100);
        print_debug("Error occurred, entering error loop...");
    }
}

/**
 * @brief Timer callback to publish encoder angle values
 */
void timer_publisher_encoders(rcl_timer_t * timer, int64_t last_call_time) {
    RCLC_UNUSED(last_call_time);
    
    if (timer != NULL) {
        publish_encoder_values();
    }
}

/**
 * @brief Publish encoder values manually
 * This function can be called from the main loop
 */
void publish_encoder_values(void) {
    // Here you should read the actual encoder values
    // For now, using example values
    
    // Example of encoder reading (replace with your reading code)
    // encoderA_angle_msg.data = read_encoder_a();
    // encoderB_angle_msg.data = read_encoder_b(); 
    // encoderC_angle_msg.data = read_encoder_c();
    
    // Publish values
    RCSOFTCHECK(rcl_publish(&encoderA_pub, &encoderA_angle_msg, NULL));
    RCSOFTCHECK(rcl_publish(&encoderB_pub, &encoderB_angle_msg, NULL));
    RCSOFTCHECK(rcl_publish(&encoderC_pub, &encoderC_angle_msg, NULL));
}

/**
 * @brief Service callback for motor control requests
 */
void service_server_movemotor(const void * srv_req, void * srv_res) {
    const custom_msg_svrs__srv__MotorControl_Request * req_in = 
        (const custom_msg_svrs__srv__MotorControl_Request *)srv_req;
    custom_msg_svrs__srv__MotorControl_Response * res_in = 
        (custom_msg_svrs__srv__MotorControl_Response *)srv_res;

    // Validate that the requested motor is within the valid range (0-2)
    if (req_in->data_uint8 >= 0 && req_in->data_uint8 < 3) {
        // Set the corresponding flag bit for the requested motor
        services_flags |= (1 << req_in->data_uint8);
        
        // Store direction and angle parameters
        dir[req_in->data_uint8] = req_in->data_bool;
        angle[req_in->data_uint8] = req_in->data_float;
    } else if (req_in->data_uint8 == 4) { 
        // Set the tool servo state
        tool_servo = req_in->data_bool;
        
        // Set the tool service flag
        services_flags |= TOOL_SERVICE;
    } else {
        // Motor index out of range
        res_in->response_message = false; // Indicate failure
        return;
    }
    // Recived 
    res_in->response_message = true; // Indicate success
}

/**
 * @brief Publish end of service message
 * 
 * This function publishes a message indicating the end of service.
 * It can be used to signal that the robot has completed its tasks.
 * 
 * @param status The status of the end of service (true for success, false for waitting)
 */
void publish_end_of_service(bool status){
    end_of_service_msg.data = status; // Set the end of service flag
    RCSOFTCHECK(rcl_publish(&end_of_service_pub, &end_of_service_msg, NULL));
}

/**
 * @brief Service callback for tool control requests
 */
// void service_server_toolcontrol(const void * srv_req, void * srv_res) {
//     const std_srvs__srv__SetBool_Request * req_in =
//         (const std_srvs__srv__SetBool_Request *)srv_req;
//     std_srvs__srv__SetBool_Response * res_in =
//         (std_srvs__srv__SetBool_Response *)srv_res;

//     // Set the tool servo state based on the request
//     tool_servo = req_in->data;
    
//     // Set the tool service flag
//     services_flags |= TOOL_SERVICE;

//     // Send confirmation response
//     res_in->success = true;
// }

/**
 * @brief Initialize all MicroROS components
 */
void setup_micro_ros_scara(void) {
    // Initialize allocator
    allocator = rcl_get_default_allocator();

    // Initialize ROS context
    print_debug("Free Heap before rclc_support_init: ");
    RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

    // Create node
    print_debug("Free Heap before rclc_node_init_default: ");
    RCCHECK(rclc_node_init_default(&node, "scara_micro_ros", "", &support));

    // Initialize message data
    encoderA_angle_msg.data = 0.0;
    encoderB_angle_msg.data = 0.0;
    encoderC_angle_msg.data = 0.0;
    end_of_service_msg.data = false; 

    // Create publishers for encoder angles
    print_debug("Initializing encoder A publisher...");
    RCCHECK(rclc_publisher_init_default(
        &encoderA_pub,
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),
        "encoderA_angle_pub"));
    
    print_debug("Initializing encoder B publisher...");
    RCCHECK(rclc_publisher_init_default(
        &encoderB_pub,
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),
        "encoderB_angle_pub"));
    
    print_debug("Initializing encoder C publisher...");
    RCCHECK(rclc_publisher_init_default(
        &encoderC_pub,
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),
        "encoderC_angle_pub"));
    
    // Create publisher for end of service
    print_debug("Initializing end of service publisher...");
    RCCHECK(rclc_publisher_init_default(
        &end_of_service_pub,
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),
        "end_of_service_pub"));

    // Create service server for motor control
    print_debug("Free Heap before move_motor_server init: ");
    RCCHECK(rclc_service_init_default(
        &move_motor_server,
        &node,
        ROSIDL_GET_SRV_TYPE_SUPPORT(custom_msg_svrs, srv, MotorControl),
        "move_X_motor"));

    // Create service server for tool control
    // print_debug("Free Heap before tool_control_server init: ");
    // RCCHECK(rclc_service_init_default(
    //     &tool_control_server,
    //     &node,
    //     ROSIDL_GET_SRV_TYPE_SUPPORT(std_srvs, srv, SetBool),
    //     "tool_control_service"));
    // print_debug("Tool control service initialized successfully");

    // Optional: Create timer for periodic publishing
    /*
    const unsigned int timer_timeout = 100; // ms
    RCCHECK(rclc_timer_init_default(
        &timer,
        &support,
        RCL_MS_TO_NS(timer_timeout),
        timer_publisher_encoders));
    */

    // Create executor and add services (2 services = 2 handles)
    RCCHECK(rclc_executor_init(&executor, &support.context, 2, &allocator)); // Set to 3 handles for two services, plus buffer

    // // Add timer if enabled
    // // RCCHECK(rclc_executor_add_timer(&executor, &timer));
    
    // --- Add services to executor ---
    // 1. Add tool control service (Keeping order in executor consistent with previous tests)
    // print_debug("Free Heap before adding tool_control_service to executor: ");
    // RCCHECK(rclc_executor_add_service(&executor, &tool_control_server, &tool_control_req, &tool_control_res, service_server_toolcontrol));
    // print_debug("-> tool_control_service added successfully to executor");

    // 2. Add motor control service
    RCCHECK(rclc_executor_add_service(&executor, &move_motor_server, &srv_req, &srv_res, service_server_movemotor));
    print_debug("Executor setup finished");
}

/**
 * @file microros_utils.cpp
 * @brief Implementation of MicroROS utilities for SCARA robot communication
 * @author Adrián Silva Palafox
 * @date May 2025
 */

#include "microros_utils.h"

// Global variables for service handling
volatile uint16_t services_flags = 0x00;  // Flags for service request tracking
volatile bool dir[3] = {0};               // Direction for each motor [base, link1, link2]
volatile float angle[3] = {0};            // Target angle for each motor [base, link1, link2]

/**
 * @brief Error handling loop
 * 
 * Enters an infinite loop when a critical ROS error occurs,
 * effectively halting the system to prevent further issues.
 */
void error_loop() {
    while(1) {
        delay(100);  // Small delay to prevent CPU hogging
    }
}

/**
 * @brief Timer callback to publish encoder angle values
 * 
 * Publishes the current angle readings from all three encoders
 * at regular intervals defined by the timer.
 * 
 * @param timer Pointer to the timer that triggered the callback
 * @param last_call_time Time since last call in nanoseconds (unused)
 */
void timer_publisher_encoders(rcl_timer_t * timer, int64_t last_call_time) {
    RCLC_UNUSED(last_call_time);
    
    if (timer != NULL) {
        // Publish all encoder angles
        RCSOFTCHECK(rcl_publish(&encoderA_pub, &encoderA_angle_msg, NULL));
        RCSOFTCHECK(rcl_publish(&encoderB_pub, &encoderB_angle_msg, NULL));
        RCSOFTCHECK(rcl_publish(&encoderC_pub, &encoderC_angle_msg, NULL));
    }
}

/**
 * @brief Service callback for motor control requests
 * 
 * Processes incoming motor control requests by setting the appropriate
 * service flags and storing direction and angle parameters.
 * 
 * @param srv_req Pointer to the request message
 * @param srv_res Pointer to the response message
 */
void service_server_movemotor(const void * srv_req, void * srv_res) {
    // Cast generic pointers to specific message types
    const custom_msg_svrs__srv__MotorControl_Request * req_in = 
        (const custom_msg_svrs__srv__MotorControl_Request *)srv_req;
    custom_msg_svrs__srv__MotorControl_Response * res_in = 
        (custom_msg_svrs__srv__MotorControl_Response *)srv_res;

    // Set the corresponding flag bit for the requested motor
    bitSet(services_flags, req_in->data_uint8);
    
    // Store direction and angle parameters
    dir[req_in->data_uint8] = req_in->data_bool;     // Direction (CW/CCW)
    angle[req_in->data_uint8] = req_in->data_float;  // Target angle
    
    // Send confirmation response
    rosidl_runtime_c__String__assign(&res_in->response_message, "Request received");
}

/**
 * @brief Initialize all MicroROS components
 * 
 * Sets up the ROS node, publishers, services, and executor
 * for the SCARA robot control system.
 */
void setup_micro_ros_scara(void) {
    // Initialize allocator
    allocator = rcl_get_default_allocator();

    // Initialize ROS context
    RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

    // Create node
    RCCHECK(rclc_node_init_default(&node, "scara_micro_ros", "", &support));

    // Create publishers for encoder angles
    RCCHECK(rclc_publisher_init_default(
        &encoderA_pub,
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),
        "encoderA_angle_pub"));
    
    RCCHECK(rclc_publisher_init_default(
        &encoderB_pub,
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),
        "encoderB_angle_pub"));
    
    RCCHECK(rclc_publisher_init_default(
        &encoderC_pub,
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),
        "encoderC_angle_pub"));

    // Create service server for motor control
    RCCHECK(rclc_service_init_default(
        &move_motor_server,
        &node,
        ROSIDL_GET_SRV_TYPE_SUPPORT(custom_msg_svrs, srv, MotorControl),
        "move_X_motor"));

    // Timer code commented out - left for reference
    /*
    // Create timer for periodic publishing
    const unsigned int timer_timeout = 100; // ms
    RCCHECK(rclc_timer_init_default(
        &timer,
        &support,
        RCL_MS_TO_NS(timer_timeout),
        timer_publisher_encoders));
    */

    // Create executor and add service
    RCCHECK(rclc_executor_init(&executor, &support.context, 2, &allocator));
    // RCCHECK(rclc_executor_add_timer(&executor, &timer));  // Commented out
    RCCHECK(rclc_executor_add_service(&executor, &move_motor_server, &srv_req, &srv_res, service_server_movemotor));
}
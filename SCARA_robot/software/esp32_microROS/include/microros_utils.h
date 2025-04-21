/**
 * @file microros_utils.h
 * @brief MicroROS utilities for SCARA robot communication
 * @author Adrián Silva Palafox
 * @date May 2025
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
#include <rosidl_runtime_c/string_functions.h>  // Required for String__assign

// ROS message types
#include <std_msgs/msg/float32.h>
#include <std_msgs/msg/u_int8.h>
#include <custom_msg_svrs/srv/motor_control.h>

/**
 * @brief Error checking macros for ROS functions
 * 
 * RCCHECK: Fatal error check that enters error loop on failure
 * RCSOFTCHECK: Non-fatal error check that continues execution
 */
#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

/**
 * @section PUBLISHERS
 * ROS Publishers for encoder angle data
 */

// Encoder A publisher (Link 1)
rcl_publisher_t encoderA_pub;
std_msgs__msg__Float32 encoderA_angle_msg;

// Encoder B publisher (Link 2)
rcl_publisher_t encoderB_pub;
std_msgs__msg__Float32 encoderB_angle_msg;

// Encoder C publisher (Base)
rcl_publisher_t encoderC_pub;
std_msgs__msg__Float32 encoderC_angle_msg;

/**
 * @section SERVICES
 * ROS Service definitions for motor control
 */

// Service flags and parameters
extern volatile uint16_t services_flags;
extern volatile bool dir[3];  // Direction for each motor
extern volatile float angle[3];  // Target angle for each motor

// Service flag bit definitions
#define MOVE_BASE_SERVICE BIT0
#define MOVE_LINK1_SERVICE BIT1
#define MOVE_LINK2_SERVICE BIT2

// Motor control service components
rcl_service_t move_motor_server;
rmw_request_id_t header_response;
custom_msg_svrs__srv__MotorControl_Request srv_req;
custom_msg_svrs__srv__MotorControl_Response srv_res;

/**
 * @section ROS_COMPONENTS
 * Core MicroROS components
 */
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

/**
 * @section FUNCTIONS
 * MicroROS utility functions
 */

/**
 * @brief Infinite loop indicating a fatal error
 * Called when a critical ROS error occurs
 */
void error_loop();

/**
 * @brief Timer callback to publish encoder values
 * 
 * @param timer Pointer to the timer that triggered the callback
 * @param last_call_time Time since last call in nanoseconds
 */
void timer_publisher_encoders(rcl_timer_t * timer, int64_t last_call_time);

/**
 * @brief Service callback for motor control requests
 * 
 * @param request_msg Pointer to the request message
 * @param response_msg Pointer to the response message
 */
void service_server_movemotor(const void * request_msg, void * response_msg);

/**
 * @brief Initialize all MicroROS components
 * Sets up node, publishers, services, and executor
 */
void setup_micro_ros_scara(void);

#ifdef __cplusplus
}
#endif

#endif // MICROROS_UTILS_H
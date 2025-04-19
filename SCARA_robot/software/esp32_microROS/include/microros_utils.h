
#ifndef MICROROS_UTILS_H
#define MICROROS_UTILS_H

#ifdef __cplusplus
extern "C" {
#endif

#include <Arduino.h>

#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

#include <std_msgs/msg/float32.h>

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

// TOPICS
// Encoder A publisher
rcl_publisher_t encoderA_pub;
std_msgs__msg__Float32 encoderA_angle_msg;
// Encoder B publisher
rcl_publisher_t encoderB_pub;
std_msgs__msg__Float32 encoderB_angle_msg;
// Encoder C publisher
rcl_publisher_t encoderC_pub;
std_msgs__msg__Float32 encoderC_angle_msg;

rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

// Functions 
void error_loop();
void timer_publisher_encoders(rcl_timer_t * timer, int64_t last_call_time);
void setup_micro_ros_scara(void);

#ifdef __cplusplus
}
#endif

#endif // MICROROS_UTILS_H
#include "microros_utils.h"

// Error handle loop
void error_loop() {
    while(1) {
      delay(100);
    }
}

// Publishes the encoders A,B,C angle message
void timer_publisher_encoders(rcl_timer_t * timer, int64_t last_call_time) {
    RCLC_UNUSED(last_call_time);
    if (timer != NULL) {
      RCSOFTCHECK(rcl_publish(&encoderA_pub, &encoderA_angle_msg, NULL));
      RCSOFTCHECK(rcl_publish(&encoderB_pub, &encoderB_angle_msg, NULL));
      RCSOFTCHECK(rcl_publish(&encoderC_pub, &encoderC_angle_msg, NULL));
    }
}

void setup_micro_ros_scara(void){
    allocator = rcl_get_default_allocator();

    //create init_options
    RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

    // create node
    RCCHECK(rclc_node_init_default(&node, "scara_micro_ros", "", &support));

    // create publishers
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

    // create timer,
    // const unsigned int timer_timeout = 100; // ms
    // RCCHECK(rclc_timer_init_default(
    //     &timer,
    //     &support,
    //     RCL_MS_TO_NS(timer_timeout),
    //     timer_publisher_encoders));

    // create executor
    RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
    // RCCHECK(rclc_executor_add_timer(&executor, &timer));
}


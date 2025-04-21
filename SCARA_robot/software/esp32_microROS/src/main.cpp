/*
 * @file main.cpp
 * @brief Micro-ROS node for controlling a SCARA robot using AS5600 encoders and Nema17 step-motors.
 * @author Adrián Silva Palafox
 * @date May 2025
 */
#include <Arduino.h>
#include <micro_ros_platformio.h>
#include "microros_utils.h"
#include "utils.hpp"

/*******
 * PROTOTYPES
 *******/
/**
 * @brief Move a motor by a specified angle
 * 
 * @param motor The DRV8825 motor driver
 * @param encoder The AS5600 magnetic encoder
 * @param encoderX_angle_msg ROS message container for publishing encoder angle
 * @param encoderX_pub ROS publisher for the encoder angle
 * @param dir Direction of rotation (true = clockwise, false = counterclockwise)
 * @param angle The angle to rotate in degrees
 */
template<typename I2CType>
void mv_ang(
    DRV8825 &motor, 
    AS5600<I2CType> &encoder, 
    std_msgs__msg__Float32 *encoderX_angle_msg, 
    rcl_publisher_t *encoderX_pub, 
    bool dir,
    float angle);

/**
 * @brief Initialize system components and communication
 */
void setup() {
    // Initialize Serial communication
    Serial.begin(115200);
    
    // Initialize micro-ROS 
    set_microros_serial_transports(Serial);
    delay(2000);
    setup_micro_ros_scara();

    // Initialize the AS5600 encoders
    setup_magnetic_encoders();

    // Initialize stepper motors
    setup_stepper_motors();
}   

/**
 * @brief Main program loop handling service requests
 */
void loop() {
    RCSOFTCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(1000)));

    switch (services_flags) {
    case MOVE_BASE_SERVICE:
        bitClear(services_flags, 0);
        mv_ang(motor_base, encoder_c, &encoderC_angle_msg, &encoderC_pub, dir[0], angle[0]);
        break;
    case MOVE_LINK1_SERVICE:
        bitClear(services_flags, 1);
        mv_ang(motor_link1, encoder_a, &encoderA_angle_msg, &encoderA_pub, dir[1], angle[1]);
        break;
    case MOVE_LINK2_SERVICE:
        bitClear(services_flags, 2);
        mv_ang(motor_link2, encoder_b, &encoderB_angle_msg, &encoderB_pub, dir[2], angle[2]);
        break;
    default:
        // Handle default case - no service request to process
        break;
    }
}

/**
 * @brief Move a motor by a specified angle with encoder feedback
 * 
 * This function rotates a stepper motor to achieve the requested angle
 * while publishing the actual position read from the encoder.
 * It manages full rotations and remaining steps separately.
 */
template<typename I2CType>
void mv_ang(DRV8825 &motor, AS5600<I2CType> &encoder, std_msgs__msg__Float32 *encoderX_angle_msg, rcl_publisher_t *encoderX_pub, bool dir, float angle)
{
    // Calculate total steps needed with proper rounding
    const uint32_t steps = static_cast<uint32_t>(round(angle * (motor.steps_full_rot / 360.0)));
    
    // Return immediately if no movement required
    if (steps == 0) return;
    
    // Enable motor driver
    motor.en_dis_driver(HIGH);

    // Timeout constant in milliseconds
    const unsigned long TIMEOUT_MS = 10000;
    
    // Handle complete rotations and remaining steps
    if (steps >= motor.steps_full_rot) {
        const uint32_t full_rotations = steps / motor.steps_full_rot;
        const uint32_t remaining_steps = steps % motor.steps_full_rot;
        
        // Process full rotations
        for (uint32_t i = 0; i < full_rotations; i++) {
            tx_done = false;
            unsigned long start_time = millis();
            
            motor.move_steps(dir, false, motor.steps_full_rot, motor.pulses_arr);
            
            // Publish current angle with timeout protection
            while (!tx_done && (millis() - start_time < TIMEOUT_MS)) {
                encoderX_angle_msg->data = encoder.read_angle();
                RCSOFTCHECK(rcl_publish(encoderX_pub, encoderX_angle_msg, nullptr));
            }
            
            // Exit loop if timeout occurred
            if (!tx_done) break;
        }
        
        // Handle remaining steps if no timeout occurred
        if (tx_done && remaining_steps > 0) {
            tx_done = false;
            unsigned long start_time = millis();
            
            motor.move_steps(dir, false, remaining_steps, motor.pulses_arr);
            
            // Publish angle with timeout protection
            while (!tx_done && (millis() - start_time < TIMEOUT_MS)) {
                encoderX_angle_msg->data = encoder.read_angle();
                RCSOFTCHECK(rcl_publish(encoderX_pub, encoderX_angle_msg, nullptr));
            }
        }
    } else {
        // Move angle less than 360 degrees
        tx_done = false;
        unsigned long start_time = millis();
        
        motor.move_steps(dir, false, steps, motor.pulses_arr);
        
        // Publish angle with timeout protection
        while (!tx_done && (millis() - start_time < TIMEOUT_MS)) {
            encoderX_angle_msg->data = encoder.read_angle();
            RCSOFTCHECK(rcl_publish(encoderX_pub, encoderX_angle_msg, nullptr));
        }
    }
    
    // Disable driver to save power and prevent overheating
    motor.en_dis_driver(LOW);
    
    // Publish final position regardless of outcome
    encoderX_angle_msg->data = encoder.read_angle();
    RCSOFTCHECK(rcl_publish(encoderX_pub, encoderX_angle_msg, nullptr));
}
/*
* @file main.cpp
* @brief Micro-ROS node for controlling a SCARA robot using AS5600 encoders and Nema17 step-motors.
* @author Adrián Silva Palafox
* @date may 2025
*/
#include <Arduino.h>

#include <micro_ros_platformio.h>
#include "microros_utils.h"

#include "utils.hpp"

/*******
PROTYPES
********/

// Move a motor N angle
template<typename I2CType>
void mv_ang(DRV8825 &motor, AS5600<I2CType> &encoder, std_msgs__msg__Float32 *encoderX_angle_msg, rcl_publisher_t *encoderX_pub, bool dir);



void setup() {
    // Initialize Serial communication
    Serial.begin(115200);
    
    // Initialize micro-ROS 
    set_microros_serial_transports(Serial);
    delay(2000);
    setup_micro_ros_scara();

    // Initialize the AS5600 encoders
    setup_magnetic_encoders();

    // Initialize step-motors
    setup_stepper_motors();
}   

void loop() {
    
    mv_ang(motor_link1, encoder_a, &encoderA_angle_msg, &encoderA_pub, true);
    mv_ang(motor_link2, encoder_b, &encoderB_angle_msg, &encoderB_pub, true);
    motor_base.move_steps(true, true, BASE_MOTOR_STEPS, pulses_base);

    RCSOFTCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));
}

// FUNCS DEFENITIONS
template<typename I2CType>
void mv_ang(DRV8825 &motor, AS5600<I2CType> &encoder, std_msgs__msg__Float32 *encoderX_angle_msg, rcl_publisher_t *encoderX_pub, bool dir)
{
    tx_done = false;
    motor.move_steps(dir, false, LINKS_MOTOR_STEPS, pulses_links);
    do {
        encoderX_angle_msg->data = encoder.read_angle();
        RCSOFTCHECK(rcl_publish(encoderX_pub, encoderX_angle_msg, nullptr));
    } while (!tx_done);  // TODO: agregar timeout si es necesario
}
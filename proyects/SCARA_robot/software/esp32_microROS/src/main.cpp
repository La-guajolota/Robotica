/*
 * @file main.cpp
 * @brief Micro-ROS node for controlling a didactic SCARA robot using AS5600 encoders and Nema17 step-motors.
 * @author Adrián Silva Palafox
 * @date May 2025
 */
#include <Arduino.h>
#include <micro_ros_platformio.h>
#include "conf_network.h"
#include "microros_utils.h"
#include "utils.hpp"

// Uncomment the desired transport method
// #define urosAgent_serial
#define urosAgent_wifi 

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
    float angle
);

void mv_(
    DRV8825 &motor, 
    bool dir,
    float angle
);

/**
 * @brief Sends a servo angle to the device via I2C communication.
 * 
 * This function validates the input angle to ensure it is within the 
 * permissible range (0 to 180 degrees). If the angle is valid, it sends 
 * the angle as a byte to the I2C slave device and prints a confirmation 
 * message to the serial monitor. If the angle is invalid, it prints an 
 * error message to the serial monitor.
 * 
 * @param angle The servo angle to send, must be between 0 and 180 degrees.
 * 
 * @note Ensure that the I2C communication is properly initialized before 
 * calling this function. The I2C slave device address should be defined 
 * as `I2C_ADDRESS`.
 */
const uint8_t I2C_ADDRESS = 0x08;
void sendServoAngle(bool command);

// --- IMPLEMENTACIÓN DE LA FUNCIÓN DE DEBUG ---
// Como estamos en un archivo .cpp, tenemos acceso a 'Serial'.
void print_debug(const char *msg) {
    Serial.println(msg);
    // Serial.println(String(ESP.getFreeHeap()));
}

void setup() {
    // Initialize Serial communication
    Serial.begin(115200);
    
    // Initialize micro-ROS
#ifdef urosAgent_serial 
    set_microros_serial_transports(Serial);
#elif defined(urosAgent_wifi)
    IPAddress agent_ip(AGENT_IP);
    size_t agent_port = AGENT_PORT;
    set_microros_wifi_transports(SSID, SSID_PW, agent_ip, agent_port);
#endif
    delay(2000);
    setup_micro_ros_scara();
    publish_end_of_service(false); // Indicate end of service

    // Initialize the AS5600 encoders
    setup_magnetic_encoders();

    // Initialize stepper motors
    setup_stepper_motors();
}   

void loop() {
    RCSOFTCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(1)));

    switch (services_flags) {
    case MOVE_BASE_SERVICE:
        bitClear(services_flags, 0);
        // mv_ang(motor_base, encoder_c, &encoderC_angle_msg, &encoderC_pub, dir[0], angle[0]);
        mv_(motor_base, dir[0], angle[0]);
        break;
    case MOVE_LINK1_SERVICE:
        bitClear(services_flags, 1);
        mv_ang(motor_link1, encoder_a, &encoderA_angle_msg, &encoderA_pub, dir[1], angle[1]);
        break;
    case MOVE_LINK2_SERVICE:
        bitClear(services_flags, 2);
        mv_ang(motor_link2, encoder_b, &encoderB_angle_msg, &encoderB_pub, dir[2], angle[2]);
        break;
    case TOOL_SERVICE:
        bitClear(services_flags, 3);
        sendServoAngle(tool_servo);
        break;
    default:
        // No service flags set, do nothing
        break;
    }

    // Publish encoder readings with null checks
    float angle = encoder_a.read_angle();
    if (!isnan(angle)) {
        encoderA_angle_msg.data = angle;
        RCSOFTCHECK(rcl_publish(&encoderA_pub, &encoderA_angle_msg, nullptr));
    }
    
    angle = encoder_b.read_angle();
    if (!isnan(angle)) {
        encoderB_angle_msg.data = angle;
        RCSOFTCHECK(rcl_publish(&encoderB_pub, &encoderB_angle_msg, nullptr));
    }       
}

/**
 * @brief Move a motor by a specified angle with encoder feedback
 * 
 * This function rotates a stepper motor to achieve the requested angle
 * while publishing the actual position read from the encoder.
 * It manages full rotations and remaining steps separately.
 * If encoder reading returns null/invalid value, it skips encoder reading.
 */
template<typename I2CType>
void mv_ang(DRV8825 &motor, AS5600<I2CType> &encoder, std_msgs__msg__Float32 *encoderX_angle_msg, rcl_publisher_t *encoderX_pub, bool dir, float angle)
{
    publish_end_of_service(false); // Indicate service is ongoing

    // Calculate total steps needed with proper rounding
    const uint32_t steps = static_cast<uint32_t>(round(angle * (motor.steps_full_rot / 360.0)));
    
    // Return immediately if no movement required
    if (steps == 0) return;
        
    // Enable motor driver
    motor.en_dis_driver(HIGH);
    
    // Handle complete rotations and remaining steps
    if (steps >= motor.steps_full_rot) {
        const uint32_t full_rotations = steps / motor.steps_full_rot;
        const uint32_t remaining_steps = steps % motor.steps_full_rot;
        
        // Process full rotations
        for (uint32_t i = 0; i < full_rotations; i++) {
            tx_done = false;
            motor.move_steps(dir, false, motor.steps_full_rot, motor.pulses_arr);
            
            // Publish current angle with timeout protection and null check
            while (!tx_done) {
                float current_angle = encoder.read_angle();
                if (!isnan(current_angle)) {
                    encoderX_angle_msg->data = current_angle;
                    RCSOFTCHECK(rcl_publish(encoderX_pub, encoderX_angle_msg, nullptr));
                }
            }
        }
        
        // Handle remaining steps
        if (remaining_steps > 0) {
            tx_done = false;                
            motor.move_steps(dir, false, remaining_steps, motor.pulses_arr);
            
            // Publish angle with timeout protection and null check
            while (!tx_done) {
                float current_angle = encoder.read_angle();
                if (!isnan(current_angle)) {
                    encoderX_angle_msg->data = current_angle;
                    RCSOFTCHECK(rcl_publish(encoderX_pub, encoderX_angle_msg, nullptr));
                }
            }
        }
    } else {
        // Move angle less than 360 degrees
        tx_done = false;        
        motor.move_steps(dir, false, steps, motor.pulses_arr);
        
        // Publish angle with timeout protection and null check
        while (!tx_done) {
            float current_angle = encoder.read_angle();
            if (!isnan(current_angle)) {
                encoderX_angle_msg->data = current_angle;
                RCSOFTCHECK(rcl_publish(encoderX_pub, encoderX_angle_msg, nullptr));
            }
        }
    }
    
    // Disable driver to save power and prevent overheating
    motor.en_dis_driver(LOW);
    
    // Publish final position with null check
    float final_angle = encoder.read_angle();
    if (!isnan(final_angle)) {
        encoderX_angle_msg->data = final_angle;
        RCSOFTCHECK(rcl_publish(encoderX_pub, encoderX_angle_msg, nullptr));
    }
    publish_end_of_service(true); // Indicate service is done
    
}

void mv_(DRV8825 &motor, bool dir, float angle)
{
    publish_end_of_service(false); // Indicate service is ongoing
    // Calculate total steps needed with proper rounding
    const uint32_t steps = static_cast<uint32_t>(round(angle * (motor.steps_full_rot / 360.0)));

    // Return immediately if no movement required
    if (steps == 0) return;
        
    // Enable motor driver
    motor.en_dis_driver(HIGH);
    
    // Handle complete rotations and remaining steps
    if (steps >= motor.steps_full_rot) {
        const uint32_t full_rotations = steps / motor.steps_full_rot;
        const uint32_t remaining_steps = steps % motor.steps_full_rot;
        
        // Process full rotations
        for (uint32_t i = 0; i < full_rotations; i++) {
            motor.move_steps(dir, true, motor.steps_full_rot, motor.pulses_arr);
        }
        
        // Handle remaining steps
        if (remaining_steps > 0) {
            motor.move_steps(dir, true, remaining_steps, motor.pulses_arr);
        }
    } else {
        // Move angle less than 360 degrees    
        motor.move_steps(dir, true, steps, motor.pulses_arr);
    }
    
    // Disable driver to save power and prevent overheating
    motor.en_dis_driver(LOW);
    publish_end_of_service(true); // Indicate service is done

}

/**
 * @brief Sends a servo angle to the device via I2C communication.
 * 
 * This function validates the input angle to ensure it is within the 
 * permissible range (0 to 180 degrees). If the angle is valid, it sends 
 * the angle as a byte to the I2C slave device and prints a confirmation 
 * message to the serial monitor. If the angle is invalid, it prints an 
 * error message to the serial monitor.
 * */
void sendServoAngle(bool command) {
    publish_end_of_service(false); // Indicate service is ongoing

    char str = command ? '0' : '1';
    tca9548a.sel_channel(0x02);          // Select the channel for I2C communication
    I2C_.beginTransmission(I2C_ADDRESS); // Start transmission to the slave 
    I2C_.write((uint8_t)str);                     // servo goes to position 0 or 1
    I2C_.endTransmission();              // End the transmission
    
    publish_end_of_service(true); // Indicate service is done
}
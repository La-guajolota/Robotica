/**
 * @file utils.hpp
 * @brief Pin definitions and component declarations for SCARA robot control
 * @author Adrián Silva Palafox
 * @date May 2025
 */

 #ifndef UTILS_HPP
 #define UTILS_HPP
 
 #include "AS5600.hpp"
 #include "DRV8825.hpp"
 
 /**
  * @section ENCODERS
  * AS5600 magnetic encoder pin definitions and external declarations
  */
 
 // AS5600 encoder A pinout (I2C hardware bus 0)
 #define SDA_PIN_a 21
 #define SCL_PIN_a 22
 extern AS5600<TwoWire> encoder_a;
 
 // AS5600 encoder B pinout (I2C hardware bus 1)
 #define SDA_PIN_b 19
 #define SCL_PIN_b 18
 extern AS5600<TwoWire> encoder_b;
 
 // AS5600 encoder C pinout (Software I2C)
 #define SDA_PIN_c 4
 #define SCL_PIN_c 15
 extern AS5600<softI2C> encoder_c;
 
 /**
  * @section MOTORS
  * Stepper motor definitions and driver configurations
  * All motors use DRV8825 drivers
  */
 
 // Standard NEMA17 step angle (degrees per full step)
 #define NEMA17_ANGLE_STEP 1.8
 
 /**
  * @subsection BASE_MOTOR
  * Base axis stepper motor pins and controller
  */
 #define BASE_MOTOR_DIR_PIN 13   // Direction control pin
 #define BASE_MOTOR_STEP_PIN 25  // Step control pin
 #define BASE_MOTOR_RST_PIN 23   // Reset pin
 extern DRV8825 motor_base;
 
 /**
  * @subsection LINK1_MOTOR
  * Link 1 axis stepper motor pins and controller
  */
 #define LINK1_MOTOR_DIR_PIN 33  // Direction control pin
 #define LINK1_MOTOR_STEP_PIN 26 // Step control pin
 #define LINK1_MOTOR_RST_PIN 17  // Reset pin
 extern DRV8825 motor_link1;
 
 /**
  * @subsection LINK2_MOTOR
  * Link 2 axis stepper motor pins and controller
  */
 #define LINK2_MOTOR_DIR_PIN 32  // Direction control pin
 #define LINK2_MOTOR_STEP_PIN 27 // Step control pin
 #define LINK2_MOTOR_RST_PIN 16  // Reset pin
 extern DRV8825 motor_link2;
 
 /**
  * @section MOTOR_SETTINGS
  * Step and microstepping configuration
  */
 // Base motor: 400 steps per revolution (1/2 microstepping mode)
 #define BASE_MOTOR_STEPS 400
 
 // Link motors: 1600 steps per revolution (1/8 microstepping mode)
 #define LINKS_MOTOR_STEPS 1600
 
 // RMT pulse pattern arrays for ESP32 hardware PWM control
 extern rmt_item32_t pulses_base[BASE_MOTOR_STEPS];
 extern rmt_item32_t pulses_links[LINKS_MOTOR_STEPS];
 
 /**
  * @section FUNCTIONS
  * Initialization functions
  */
 
 /**
  * @brief Initialize stepper motors and their timing profiles
  */
 void setup_stepper_motors();
 
 /**
  * @brief Initialize and configure the magnetic encoders
  */
 void setup_magnetic_encoders();
 
 #endif // UTILS_HPP
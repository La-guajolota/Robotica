/**
 * @file utils.hpp
 * @brief Component definitions and utility functions for SCARA robot control
 * @author Adrián Silva Palafox
 * @date May 2025
 */

#include "utils.hpp"

 /****************** 
  * Objects Instances 
  ******************/
 
 // I2C busses instances
 TwoWire I2C_a = TwoWire(0);
 TwoWire I2C_b = TwoWire(1);
 softI2C I2C_c(SDA_PIN_c, SCL_PIN_c);  // Soft I2C bus
 
 // AS5600 encoders instances
 AS5600<TwoWire> encoder_a(SDA_PIN_a, SCL_PIN_a, &I2C_a);
 AS5600<TwoWire> encoder_b(SDA_PIN_b, SCL_PIN_b, &I2C_b);
 AS5600<softI2C> encoder_c(SDA_PIN_c, SCL_PIN_c, &I2C_c);
 
 /**
  * Encoder configuration values based on AS5600 datasheet
  * Reference: https://files.seeedstudio.com/wiki/Grove-12-bit-Magnetic-Rotary-Position-Sensor-AS5600/res/Magnetic%20Rotary%20Position%20Sensor%20AS5600%20Datasheet.pdf
  */
 uint8_t encoders_congig[writable_reg] = {
     0x00,       // ZPOS_H - Zero position high byte
     0x00,       // ZPOS_L - Zero position low byte
     0x00,       // MPOS_H - Maximum position high byte
     0x00,       // MPOS_L - Maximum position low byte
     0x00,       // MANG_H - Maximum angle high byte
     0x00,       // MANG_L - Maximum angle low byte
     0b00001100, // CONF_H - Configuration high byte
     0x00        // CONF_L - Configuration low byte
 };
 
 // Stepper motors instances
 rmt_item32_t pulses_base[BASE_MOTOR_STEPS];
 DRV8825 motor_base(
     BASE_MOTOR_DIR_PIN, 
     BASE_MOTOR_STEP_PIN, 
     BASE_MOTOR_RST_PIN, 
     RMT_CHANNEL_0, 
     BASE_MOTOR_STEPS,
     pulses_base
 );
 
 rmt_item32_t pulses_links[LINKS_MOTOR_STEPS];
 DRV8825 motor_link1(
     LINK1_MOTOR_DIR_PIN, 
     LINK1_MOTOR_STEP_PIN, 
     LINK1_MOTOR_RST_PIN, 
     RMT_CHANNEL_1, 
     LINKS_MOTOR_STEPS, 
     pulses_links
 );
 
 DRV8825 motor_link2(
     LINK2_MOTOR_DIR_PIN, 
     LINK2_MOTOR_STEP_PIN, 
     LINK2_MOTOR_RST_PIN, 
     RMT_CHANNEL_2, 
     LINKS_MOTOR_STEPS, 
     pulses_links
 );
 
 /****************************** 
  * Function Implementations 
  *******************************/
 
 /**
  * @brief Creates RMT timing chunks for stepper motor control
  * 
  * @param pulses Pointer to RMT items array
  * @param len Length of the RMT items array
  * @param rpm Motor speed in rotations per minute
  * @param microstepsPerStep Microstepping ratio (1, 2, 4, 8, 16, etc.)
  * @param stepAngleDeg Motor step angle in degrees (typically 1.8° for NEMA17)
  */
 void create_RMT_chunck(
     rmt_item32_t *pulses, 
     uint16_t len, 
     float rpm, 
     float microstepsPerStep, 
     float stepAngleDeg
 ) {
     // Calculate step frequency in Hz
     float f_step = (rpm * 360.0f * microstepsPerStep) / (60.0f * stepAngleDeg);
     
     // Calculate half period in microseconds
     float half_period_us = (1e6f / f_step) * 0.5f;
     
     // Convert to ticks (1 tick = 1µs)
     uint16_t ticks = (uint16_t)(half_period_us + 0.5f);  // With rounding
     
     // Fill the array with pulse timing information
     for (int i = 0; i < len; i++) {
         // High for half_period ticks, low for half_period ticks
         pulses[i] = rmt_item32_t{ticks, 1, ticks, 0};
     }
 }
 
 /**
  * @brief Initializes stepper motors and their timing profiles
  * 
  * Sets up the pulse patterns for the base and link motors with
  * appropriate speeds and microstepping configurations.
  */
 void setup_stepper_motors() {
     // Initialize the RMT pulse items for base motor (faster)
     create_RMT_chunck(
         pulses_base, 
         BASE_MOTOR_STEPS, 
         240,         // 240 RPM
         MICROSTEP_2, // Half-stepping
         NEMA17_ANGLE_STEP
     );
     
     // Initialize the RMT pulse items for link motors (slower)
     create_RMT_chunck(
         pulses_links, 
         LINKS_MOTOR_STEPS, 
         10,          // 10 RPM
         MICROSTEP_8, // 1/8 microstepping
         NEMA17_ANGLE_STEP
     );
     
     // Register the callback for RMT transmission end
     rmt_register_tx_end_callback(tx_end_callback, NULL);
 }
 
 /**
  * @brief Initializes and configures the magnetic encoders
  * 
  * Applies the same configuration to all three AS5600 encoders
  */
 void setup_magnetic_encoders() {
     encoder_a.set_encoder_config(encoders_congig);
     encoder_b.set_encoder_config(encoders_congig);
     encoder_c.set_encoder_config(encoders_congig);
 }
 
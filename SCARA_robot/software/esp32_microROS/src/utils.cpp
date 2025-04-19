#include "utils.hpp"

/******************
Objects' instances
*******************/
// I2C busses instances
TwoWire I2C_a = TwoWire(0); 
TwoWire I2C_b = TwoWire(1);
softI2C I2C_c(SDA_PIN_c, SCL_PIN_c);  // Soft I2C bus

// AS5600 encoders instances
AS5600<TwoWire> encoder_a(SDA_PIN_a, SCL_PIN_a, DIR_PIN_a, &I2C_a);
AS5600<TwoWire> encoder_b(SDA_PIN_b, SCL_PIN_b, DIR_PIN_b, &I2C_b);
AS5600<softI2C> encoder_c(SDA_PIN_c, SCL_PIN_c, DIR_PIN_c, &I2C_c);

// REFERENCE https://files.seeedstudio.com/wiki/Grove-12-bit-Magnetic-Rotary-Position-Sensor-AS5600/res/Magnetic%20Rotary%20Position%20Sensor%20AS5600%20Datasheet.pdf
uint8_t encoders_congig[writable_reg] = {
    0x00, // ZPOS_H
    0x00, // ZPOS_L
    0x00, // MPOS_H
    0x00, // MPOS_L
    0x00, // MANG_H
    0x00, // MANG_L
    0b00001100, // CONF_H
    0x00, // CONF_L
}; // Configuration data for the encoders

// Stepper motors instances
DRV8825 motor_base(BASE_MOTOR_DIR_PIN, BASE_MOTOR_STEP_PIN, RMT_CHANNEL_0);
DRV8825 motor_link1(LINK1_MOTOR_DIR_PIN, LINK1_MOTOR_STEP_PIN, RMT_CHANNEL_1);
DRV8825 motor_link2(LINK2_MOTOR_DIR_PIN, LINK2_MOTOR_STEP_PIN, RMT_CHANNEL_2);

//
rmt_item32_t pulses_links[LINKS_MOTOR_STEPS]; 
rmt_item32_t pulses_base[BASE_MOTOR_STEPS];

/******************************
User's functions implementation
*******************************/

// STEP MOTORS FUNCS
// Populates RMT items
void create_RMT_chunck(rmt_item32_t *pulses, uint16_t len, float rpm, float microstepsPerStep, float stepAngleDeg){

  float f_step = (rpm * 360.0f * microstepsPerStep)
               / (60.0f * stepAngleDeg) ;  //hz

  float half_period_us = (1e6f / f_step) * 0.5f;

  uint16_t ticks = (uint16_t)(half_period_us + 0.5f);  // redondeo and 1tick -> 1us 

  for (int i = 0; i < len; i++)
  {
    // High for half_period ticks, low for half_period ticks
    pulses[i] = rmt_item32_t{ticks, 1, ticks, 0};  
  }
}

void setup_stepper_motors(){
  // Initialize the RMT pulse items (RPM per motor)
  create_RMT_chunck(pulses_base, BASE_MOTOR_STEPS, 240, MICROSTEP_2, NEMA17_ANGLE_STEP);  
  create_RMT_chunck(pulses_links, LINKS_MOTOR_STEPS, 10, MICROSTEP_8, NEMA17_ANGLE_STEP); 
  
  // enable ISR relative to TX rmt
  rmt_register_tx_end_callback(tx_end_callback, NULL);
}

// MAGNETIC ENCODERS FUNCS
void setup_magnetic_encoders(){
  encoder_a.set_encoder_config(encoders_congig);
  encoder_b.set_encoder_config(encoders_congig);
  encoder_c.set_encoder_config(encoders_congig);
}


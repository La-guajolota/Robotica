#ifndef UTILS_HPP
#define UTILS_HPP

#include "AS5600.hpp"
#include "DRV8825.hpp"

// AS5600_a pinout
#define SDA_PIN_a 21
#define SCL_PIN_a 22
#define DIR_PIN_a 23
extern AS5600<TwoWire> encoder_a;

// AS5600_b pinout
#define SDA_PIN_b 19
#define SCL_PIN_b 18
#define DIR_PIN_b 5
extern AS5600<TwoWire> encoder_b;

// AS5600_c pinout
#define SDA_PIN_c 4
#define SCL_PIN_c 15
#define DIR_PIN_c 2
extern AS5600<softI2C> encoder_c;

/*****************************************
STEP-MOTORS they all are driven by DRV8825 
******************************************/ 
// Nema17
#define NEMA17_ANGLE_STEP 1.8

// Nema17 stepper motor BASE axis
#define BASE_MOTOR_DIR_PIN 13
#define BASE_MOTOR_STEP_PIN 25
extern DRV8825 motor_base;

// Nema17 stepper motor link1 axis
#define LINK1_MOTOR_DIR_PIN 33
#define LINK1_MOTOR_STEP_PIN 26
extern DRV8825 motor_link1;

// Nema17 stepper motor link2 axis
#define LINK2_MOTOR_DIR_PIN 32
#define LINK2_MOTOR_STEP_PIN 27
extern DRV8825 motor_link2;

// Settings
#define BASE_MOTOR_STEPS 400 // it is hardwired in 1/2 microstepping mode
#define LINKS_MOTOR_STEPS 1600 // They are hardwired in 1/8 microstepping mode
extern rmt_item32_t pulses_base[BASE_MOTOR_STEPS];
extern rmt_item32_t pulses_links[LINKS_MOTOR_STEPS]; 


/*****************************************
USER'S FUNCTIONS 
******************************************/ 
// Stepper motors
void setup_stepper_motors();
// Magnetic encoders
void setup_magnetic_encoders();

#endif // UTILS_HPP
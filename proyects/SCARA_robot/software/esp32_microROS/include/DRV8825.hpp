// DRV8825 Stepper Motor Driver Header File
// Datasheet: https://www.ti.com/lit/ds/symlink/drv8825.pdf

#ifndef DRV8825_HPP
#define DRV8825_HPP

#include <Arduino.h>
#include "driver/rmt.h"

// Microstepping modes
#define MICROSTEP_FULL  0
#define MICROSTEP_2     2.0
#define MICROSTEP_8     8.0
#define MICROSTEP_16    16.0
#define MICROSTEP_32    32.0

extern bool tx_done;

class DRV8825 {
private:
    uint8_t dir_pin;   // Direction pin
    uint8_t step_pin;  // Step pin

public:
    
    uint8_t rst_pin;
    uint16_t steps_full_rot;
    rmt_item32_t* pulses_arr; // 
    rmt_channel_t used_chnn;    // RMT channel used for pulse generation

    // Constructor
    DRV8825(uint8_t dir, uint8_t step, uint8_t rst, rmt_channel_t chnn, uint16_t steps_rot, rmt_item32_t* pulses_arr);

    // Methods
    void en_dis_driver(bool en_dis);
    void move_steps(bool direction, bool wait, uint16_t steps, rmt_item32_t* pulse_array); // Move motor steps
};

// RMT transmission end callback
void IRAM_ATTR tx_end_callback(rmt_channel_t chnn, void* arg);

#endif // DRV8825_HPP

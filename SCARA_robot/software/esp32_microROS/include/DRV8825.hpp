// https://www.ti.com/lit/ds/symlink/drv8825.pdf

#ifndef DRV8825_HPP
#define DRV8825_HPP

#include <Arduino.h>
#include "driver/rmt.h"

// Micro steppings modes
#define MICROSTEP_FULL 0
#define MICROSTEP_2    2.0
#define MICROSTEP_8    8.0
#define MICROSTEP_16   16.0
#define MICROSTEP_32   32.0

extern bool tx_done;

class DRV8825
{
private:
    uint8_t dir_pin;
    uint8_t step_pin;
    
public:
     
    rmt_channel_t used_chnn;

    // Constructor
    DRV8825(uint8_t dir, uint8_t step, rmt_channel_t chnn);

    // Methods
    void move_steps(bool dir , bool wait, uint16_t steps, rmt_item32_t *pulse_arr); // Array to store RMT pulse items
};

//
void IRAM_ATTR tx_end_callback(rmt_channel_t channel, void* arg);

#endif
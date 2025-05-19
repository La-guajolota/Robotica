#include "DRV8825.hpp"

bool tx_done = false;
void IRAM_ATTR tx_end_callback(rmt_channel_t channel, void* arg)
{
    tx_done = true; // Sending pulses was done finally
}

DRV8825::DRV8825(uint8_t dir, uint8_t step, uint8_t rst, rmt_channel_t chnn, uint16_t steps_rot, rmt_item32_t* pulses_arr)
    : dir_pin(dir), step_pin(step), rst_pin(rst),used_chnn(chnn), steps_full_rot(steps_rot), pulses_arr(pulses_arr)
{
    // DIR_PIN
    pinMode(dir_pin, OUTPUT);
    // RST_PIN
    pinMode(rst_pin, OUTPUT);

    // SETTING FOR STEP_PIN
    // Generic configuration for RMT channel 
    rmt_config_t cfg = {
        .rmt_mode       = RMT_MODE_TX,           // Set RMT to transmit mode
        .channel        = used_chnn,             // Assign channel x
        .gpio_num       = (gpio_num_t)step_pin,  // GPIO pin for output
        .clk_div        = 80,                    // Clock divider (80 MHz / 80 = 1 µs tick)
        .mem_block_num  = 1                      // Memory block size (up to 64 symbols)
    };

    // Configure and install each RMT channel
    rmt_config(&cfg);

    // Enable interrupts
    rmt_driver_install(cfg.channel, 0, 0);  // Install driver for channel
};

void DRV8825::en_dis_driver(bool en_dis)
{
    digitalWrite(rst_pin, en_dis);
    delay(1);
}

void DRV8825::move_steps(bool dir, bool wait, uint16_t steps,rmt_item32_t *pulse_arr)
{

    // Choose direction
    digitalWrite(dir_pin, dir);
    delay(1);

    // send pulses (number of steps) to driver
    rmt_write_items(used_chnn, pulse_arr, steps, wait);
}

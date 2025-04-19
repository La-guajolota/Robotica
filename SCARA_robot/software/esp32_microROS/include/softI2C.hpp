#ifndef SOFTI2C_HPP
#define SOFTI2C_HPP

#include <Arduino.h>

class softI2C
{
private:
    uint8_t sda_pin;
    uint8_t scl_pin;
    uint32_t clock_frequency;

    uint8_t recived_bytes = 0;
    uint8_t Rx_buffer[32] = {0}; // used to store the data received from the slave
    uint8_t read_sda(bool ack);

    public:

    // Constructor
    softI2C(uint8_t sda, uint8_t scl);

    // methods

    void begin(uint8_t sda_pin, uint8_t scl_pin, uint32_t SCL_FREQ);
    
    void beginTransmission(uint8_t address);
    void write(uint8_t data);
    void endTransmission();

    uint8_t requestFrom(uint8_t address, uint8_t quantity);
    uint8_t read();

};


#endif // SOFTI2C_HPP
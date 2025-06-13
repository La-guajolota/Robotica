/**
 * @file TCA9548A.cpp
 * @brief Implementation of the TCA9548A I2C multiplexer driver.
 * 
 * This file contains the implementation of the methods defined in the TCA9548A class.
 * The TCA9548A class provides an interface to control the TCA9548A I2C multiplexer, 
 * allowing the selection of different I2C channels for communication.
 * 
 * @author Adrián Silva Palafox
 * @date May 2025
 */

#include "TCA9548A.hpp"

/**
 * @brief Constructor for the TCA9548A class.
 * 
 * Initializes the TCA9548A multiplexer with the specified I2C address, 
 * SDA and SCL pins, and the I2C port.
 * 
 * @param address I2C address of the TCA9548A multiplexer.
 * @param sda SDA pin for the I2C bus.
 * @param scl SCL pin for the I2C bus.
 * @param rst Reset pin for the multiplexer.
 * @param i2c_port Pointer to the I2C port used for communication.
 */
TCA9548A::TCA9548A(uint8_t address, uint8_t sda, uint8_t scl, uint8_t rst, TwoWire *i2c_port)
    : address(address), sda_pin(sda), scl_pin(scl), rst_pin(rst), i2c_port(i2c_port)
{    
    pinMode(rst_pin, OUTPUT); // Set the reset pin as output
    digitalWrite(rst_pin, HIGH);
    i2c_port->begin(sda_pin, scl_pin); // Initialize the I2C port with the specified pins
}

/**
 * @brief Selects a specific channel on the TCA9548A multiplexer.
 * 
 * This method sends a command to the TCA9548A to enable communication 
 * on the specified channel. Only one channel can be active at a time.
 * 
 * @param channel The channel to select (0-7).
 */
void TCA9548A::sel_channel(uint8_t channel) {
    if (channel > 7) return; // Check if the channel is valid (0-7)

    i2c_port->beginTransmission(address); // Begin communication with the multiplexer
    i2c_port->write(1 << channel);        // Send the command to select the channel
    i2c_port->endTransmission();          // End the transmission
}


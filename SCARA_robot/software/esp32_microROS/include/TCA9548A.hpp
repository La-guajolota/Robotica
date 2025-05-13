/**
 * @file TCA9548A.hpp
 * @brief Driver class for the TCA9548A I2C multiplexer.
 * 
 * This class provides an interface to control the TCA9548A I2C multiplexer, 
 * allowing the selection of different I2C channels for communication. 
 * It is designed to work with the Arduino framework and supports the use 
 * of custom I2C ports.
 * 
 * @author Adrián Silva Palafox
 * @date May 2025
 */

#ifndef TCA9548A_HPP
#define TCA9548A_HPP

#include <Arduino.h>
#include <Wire.h>

//The default address is 0x70 when all address pins (A0, A1, A2) are set to 0.
#define TCA9548A_ADDRESS 0x70

/**
 * @class TCA9548A
 * @brief A class to control the TCA9548A I2C multiplexer.
 * 
 * The TCA9548A is an I2C multiplexer that allows multiple I2C devices with 
 * the same address to be connected to a single I2C bus. This class provides 
 * methods to initialize the multiplexer and select specific channels for communication.
 */
class TCA9548A {
private:
    uint8_t address;   ///< I2C address of the TCA9548A multiplexer.
    uint8_t sda_pin;   ///< SDA pin for the I2C bus.
    uint8_t scl_pin;   ///< SCL pin for the I2C bus.
    uint8_t rst_pin;   ///< Reset pin for the multiplexer 
    TwoWire *i2c_port; ///< Pointer to the I2C port used for communication.

public:
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
    TCA9548A(uint8_t address, uint8_t sda, uint8_t scl, uint8_t rst, TwoWire *i2c_port);

    /**
     * @brief Selects a specific channel on the TCA9548A multiplexer.
     * 
     * This method sends a command to the TCA9548A to enable communication 
     * on the specified channel. Only one channel can be active at a time.
     * 
     * @param channel The channel to select (0-7).
     */
    void sel_channel(uint8_t channel);
};

#endif // TCA9548A_HPP
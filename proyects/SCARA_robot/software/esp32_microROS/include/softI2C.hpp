/**
 * @file softI2C.hpp
 * @brief Header file for the software-based I2C driver.
 * 
 * This class provides a software-based implementation of the I2C protocol, 
 * allowing communication with I2C devices using GPIO pins for SDA and SCL lines.
 * 
 * @note The implementation is incomplete and may not fully comply with the I2C protocol. 
 * It requires further testing and debugging to ensure proper functionality.
 * 
 * @warning Use this class with caution, as it may cause issues with certain devices 
 * or under specific conditions due to its partial implementation.
 * 
 * @author Adrián Silva Palafox
 * @date APR 2025
 */
#ifndef SOFTI2C_HPP
#define SOFTI2C_HPP

#include <Arduino.h>

class softI2C
{
private:
    uint8_t sda_pin;           ///< GPIO pin used for the SDA line.
    uint8_t scl_pin;           ///< GPIO pin used for the SCL line.
    uint32_t clock_frequency;  ///< Clock frequency for the I2C bus.

    uint8_t recived_bytes = 0; ///< Number of bytes received from the slave device.
    uint8_t Rx_buffer[32] = {0}; ///< Buffer to store data received from the slave device.

    /**
     * @brief Reads a byte from the SDA line.
     * 
     * Reads a single byte of data from the SDA line and optionally sends an acknowledgment.
     * 
     * @param ack Whether to send an acknowledgment (true) or not (false).
     * @return The byte of data read from the SDA line.
     */
    uint8_t read_sda(bool ack);

public:
    /**
     * @brief Constructor for the `softI2C` class.
     * 
     * Initializes the SDA and SCL pins for the software I2C interface.
     * 
     * @param sda GPIO pin for SDA.
     * @param scl GPIO pin for SCL.
     */
    softI2C(uint8_t sda, uint8_t scl);

    /**
     * @brief Initializes the software I2C interface.
     * 
     * Configures the SDA and SCL pins as open-drain outputs and sets the clock frequency.
     * 
     * @param sda_pin GPIO pin for SDA.
     * @param scl_pin GPIO pin for SCL.
     * @param SCL_FREQ Clock frequency for the I2C bus.
     */
    void begin(uint8_t sda_pin, uint8_t scl_pin, uint32_t SCL_FREQ);

    /**
     * @brief Begins an I2C transmission to a specific address.
     * 
     * Sends the start condition and the 7-bit address of the target device.
     * 
     * @param address 7-bit I2C address of the target device.
     */
    void beginTransmission(uint8_t address);

    /**
     * @brief Writes a byte of data to the I2C bus.
     * 
     * Sends a single byte of data to the target device.
     * 
     * @param data Byte of data to send.
     */
    void write(uint8_t data);

    /**
     * @brief Ends the current I2C transmission.
     * 
     * Sends the stop condition to release the I2C bus.
     */
    void endTransmission();

    /**
     * @brief Requests data from a target device.
     * 
     * Sends a request to the target device and reads the specified number of bytes.
     * 
     * @param address 7-bit I2C address of the target device.
     * @param quantity Number of bytes to request.
     * @return The number of bytes received.
     */
    uint8_t requestFrom(uint8_t address, uint8_t quantity);

    /**
     * @brief Reads a byte of data from the I2C bus.
     * 
     * Reads a single byte of data from the target device.
     * 
     * @return The byte of data read from the I2C bus.
     */
    uint8_t read();
};

#endif // SOFTI2C_HPP
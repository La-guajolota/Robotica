/**
 * @file softI2C.cpp
 * @brief Implementation of a software-based I2C driver.
 * 
 * This file contains the implementation of the `softI2C` class, which provides 
 * a software-based I2C communication interface. It is designed to emulate I2C 
 * communication using GPIO pins for SDA and SCL lines.
 * 
 * @note The implementation is partially complete and may not function correctly 
 * in all scenarios. It requires further testing, debugging, and optimization 
 * to ensure proper operation in embedded systems.
 * 
 * @warning This code may not fully comply with the I2C protocol specifications 
 * and could cause issues with certain devices or under specific conditions.
 * 
 * @author Adrián Silva Palafox
 * @date APR 2025
 */

#include "softI2C.hpp"

/**
 * @brief Initializes the software I2C interface.
 * 
 * Configures the SDA and SCL pins as open-drain outputs and sets the clock frequency.
 * 
 * @param sda_pin GPIO pin for SDA.
 * @param scl_pin GPIO pin for SCL.
 * @param SCL_FREQ Clock frequency for the I2C bus.
 */
void softI2C::begin(uint8_t sda_pin, uint8_t scl_pin, uint32_t SCL_FREQ) {
    pinMode(sda_pin, OUTPUT_OPEN_DRAIN);
    pinMode(scl_pin, OUTPUT_OPEN_DRAIN);
    digitalWrite(sda_pin, HIGH);
    digitalWrite(scl_pin, HIGH);
    clock_frequency = SCL_FREQ; 
}

/**
 * @brief Constructor for the `softI2C` class.
 * 
 * Initializes the SDA and SCL pins for the software I2C interface.
 * 
 * @param sda GPIO pin for SDA.
 * @param scl GPIO pin for SCL.
 */
softI2C::softI2C(uint8_t sda, uint8_t scl) 
    : sda_pin(sda), scl_pin(scl) {
}

/**
 * @brief Begins an I2C transmission to a specific address.
 * 
 * Sends the start condition and the 7-bit address of the target device.
 * 
 * @param address 7-bit I2C address of the target device.
 */
void softI2C::beginTransmission(uint8_t address) {
    // Set SDA and SCL to set high before starting
    digitalWrite(sda_pin, HIGH);
    digitalWrite(scl_pin, HIGH);
    delayMicroseconds(1);

    // Start condition
    digitalWrite(sda_pin, LOW);
    delayMicroseconds(4); 
    digitalWrite(scl_pin, LOW);
    delayMicroseconds(2);

    // Send address
    for (int i = 1; i < 8; i++) { // !!! i = 1 
        // Put bit on SDA
        digitalWrite(sda_pin, ((address << i) & 0x80) ? HIGH : LOW);
        delayMicroseconds(1);

        // Clock the SCL line
        digitalWrite(scl_pin, HIGH);
        delayMicroseconds(4); 
        digitalWrite(scl_pin, LOW);
        delayMicroseconds(1);
    }    

    // send the write bit
    delayMicroseconds(1);
    digitalWrite(sda_pin, LOW);

    // clock the SCL line so the slave can write mode bit
    for (size_t i = 0; i < 2; i++)
    {
        digitalWrite(scl_pin, HIGH);
        delayMicroseconds(2);
        digitalWrite(scl_pin, LOW);
        delayMicroseconds(2);
    }
}

/**
 * @brief Ends the current I2C transmission.
 * 
 * Sends the stop condition to release the I2C bus.
 */
void softI2C::endTransmission() {
    // Stop condition
    digitalWrite(sda_pin, LOW);
    digitalWrite(scl_pin, HIGH);
    delayMicroseconds(2); 
    digitalWrite(sda_pin, HIGH);
    delayMicroseconds(2);
}

/**
 * @brief Writes a byte of data to the I2C bus.
 * 
 * Sends a single byte of data to the target device.
 * 
 * @param data Byte of data to send.
 */
void softI2C::write(uint8_t data) {    
    // Send data
    for (int i = 0; i < 8; i++) {
        digitalWrite(sda_pin, ((data << i) & 0x80) ? HIGH : LOW);
        delayMicroseconds(2); 
        
        digitalWrite(scl_pin, HIGH);
        delayMicroseconds(4);

        digitalWrite(scl_pin, LOW);
        delayMicroseconds(1); 
    }

    bool ack = false;
    // read acknowledge
    digitalWrite(sda_pin, HIGH);
    digitalWrite(scl_pin, HIGH);
    delayMicroseconds(2);
    ack = digitalRead(sda_pin);
    digitalWrite(scl_pin, LOW);
}

/**
 * @brief Reads a byte from the SDA line.
 * 
 * Reads a single byte of data from the SDA line and sends an acknowledgment.
 * 
 * @param ack Whether to send an acknowledgment (true) or not (false).
 * @return The byte of data read from the SDA line.
 */
uint8_t softI2C::read_sda(bool ack){
    uint8_t data_byte = 0;
    digitalWrite(sda_pin, HIGH);
    
    for( uint8_t i =0; i<8; i++){
        data_byte <<= 1;

        do{
            digitalWrite(scl_pin, HIGH);
        }while(digitalRead(scl_pin) == 0);  //clock stretching
        
        delayMicroseconds(4);
        if(digitalRead(sda_pin)) data_byte |=1;
        
        delayMicroseconds(4);
        digitalWrite(scl_pin, LOW);
    }

    digitalWrite(sda_pin, ack ? LOW : HIGH );
    digitalWrite(scl_pin, HIGH);
    delayMicroseconds(4);
    digitalWrite(scl_pin, LOW);
    digitalWrite(sda_pin, HIGH);

    return(data_byte);
}

/**
 * @brief Requests data from a target device.
 * 
 * Sends a request to the target device and reads the specified number of bytes.
 * 
 * @param address 7-bit I2C address of the target device.
 * @param quantity Number of bytes to request.
 * @return The number of bytes received.
 */
uint8_t softI2C::requestFrom(uint8_t address, uint8_t quantity){
    recived_bytes = 0;

    // Set SDA and SCL to set high before starting
    digitalWrite(sda_pin, HIGH);
    digitalWrite(scl_pin, HIGH);
    delayMicroseconds(1);

    // Start condition
    digitalWrite(sda_pin, LOW);
    delayMicroseconds(4); 
    digitalWrite(scl_pin, LOW);
    delayMicroseconds(2);

    // Send address
    for (int i = 1; i < 8; i++) { // !!! i = 1 
        // Put bit on SDA
        digitalWrite(sda_pin, ((address << i) & 0x80) ? HIGH : LOW);
        delayMicroseconds(1);

        // Clock the SCL line
        digitalWrite(scl_pin, HIGH);
        delayMicroseconds(4); 
        digitalWrite(scl_pin, LOW);
        delayMicroseconds(1);
    }    

    // send the read bit
    digitalWrite(sda_pin, HIGH); 
    delayMicroseconds(1);
    
    // clock the SCL line so the slave can write mode bit
    digitalWrite(scl_pin, HIGH);
    delayMicroseconds(2);
    digitalWrite(scl_pin, LOW);
    digitalWrite(sda_pin, LOW);
    delayMicroseconds(2);
    digitalWrite(scl_pin, HIGH);
    delayMicroseconds(2);
    digitalWrite(scl_pin, LOW);
    delayMicroseconds(2);
    digitalWrite(scl_pin, HIGH);

    // READ DATA FROM SLAVE
    for (uint8_t i = 0; i < quantity; i++)
    {
        Rx_buffer[i] = read_sda((i==quantity-1)? LOW:HIGH);
        recived_bytes++;
    }

    endTransmission();

    return recived_bytes;
}

/**
 * @brief Reads a byte of data from the I2C bus.
 * 
 * Reads a single byte of data from the target device.
 * 
 * @return The byte of data read from the I2C bus.
 */
uint8_t softI2C::read() {
    uint8_t data_buyte = Rx_buffer[recived_bytes-1];
    recived_bytes--;

    return data_buyte;
}
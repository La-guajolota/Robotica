#ifndef AS5600_HPP
#define AS5600_HPP

#include <Arduino.h>
#include <Wire.h>
#include <softI2C.hpp>

/*****************************************
MAGNETIC ENCODERS AS5600 
https://files.seeedstudio.com/wiki/Grove-12-bit-Magnetic-Rotary-Position-Sensor-AS5600/res/Magnetic%20Rotary%20Position%20Sensor%20AS5600%20Datasheet.pdf
******************************************/
// MEMORY MAP CONFIG REGISTERS
#define ZMCO         0x00
#define ZPOS_H       0x01
#define ZPOS_L       0x02
#define MPOS_H       0x03
#define MPOS_L       0x04
#define MANG_H       0x05
#define MANG_L       0x06
#define CONF_H       0x07
#define CONF_L       0x08
// MEMORY MAP OUTPUT REGISTERS
#define RAW_ANGLE_H  0x0C
#define RAW_ANGLE_L  0x0D
#define ANGLE_H      0x0E
#define ANGLE_L      0x0F
// MEMORY MAP STATUS REGISTERS
#define STATUS       0x0B
#define AGC          0x1A
#define MAGNITUDE_H  0x1B
#define MAGNITUDE_L  0x1C
// MEMORY MAP BURN COMMAND
#define BURN         0xFF

#define SCL_FREQ 1000000    //1Mhz
const int8_t readable_reg = 17;
const int8_t writable_reg = 8;
const int8_t i2c_address = 0x36;
const float  AS5600_RAW_TO_DEGREES  = 360.0 / 4096;

/**
 * @class AS5600
 * @brief Driver class for the AS5600 magnetic rotary position sensor.
 * 
 * This class provides an interface to configure and read data from the AS5600 sensor
 * using the I2C communication protocol. It allows reading the angular position and 
 * configuring the encoder settings.
 */
template<typename I2CType>
class AS5600 {
private:
    uint8_t sda_pin;
    uint8_t scl_pin;
    I2CType *I2C_port;

    uint16_t readReg(uint8_t reg);
    void writeReg(uint8_t reg, uint16_t data);

public:
    uint8_t data[readable_reg] = {0};

    AS5600(uint8_t sda, uint8_t scl, I2CType *I2C_port);
    float read_angle();
    void set_encoder_config(uint8_t *data_config);
};

// Implementación de la plantilla

template<typename I2CType>
AS5600<I2CType>::AS5600(uint8_t sda, uint8_t scl, I2CType *I2C_port)
    : sda_pin(sda), scl_pin(scl), I2C_port(I2C_port)
{
    I2C_port->begin(sda_pin, scl_pin, SCL_FREQ);
}

template<typename I2CType>
uint16_t AS5600<I2CType>::readReg(uint8_t reg) {
    I2C_port->beginTransmission(i2c_address);
    I2C_port->write(reg);
    I2C_port->endTransmission();

    uint8_t nbytes = I2C_port->requestFrom(i2c_address, 2);
    uint16_t data = 0;

    if (nbytes == 2) {
        data = I2C_port->read() << 8; // Read the high byte and shift it
        data |= I2C_port->read();    // Read the low byte and combine
    }
    return data;
}

template<typename I2CType>
void AS5600<I2CType>::writeReg(uint8_t reg, uint16_t data) {
    I2C_port->beginTransmission(i2c_address);
    I2C_port->write(reg);
    I2C_port->write(data >> 8);
    I2C_port->write(data & 0xFF);
    I2C_port->endTransmission();
}

template<typename I2CType>
float AS5600<I2CType>::read_angle() {
    uint16_t angle = (4096 - readReg(ANGLE_H)) & 0x0FFF;
    return angle * AS5600_RAW_TO_DEGREES; // Convertir a grados
}

template<typename I2CType>
void AS5600<I2CType>::set_encoder_config(uint8_t *data_config) {
    writeReg(ZPOS_H, (data_config[0] << 8) | data_config[1]);
    writeReg(MPOS_H, (data_config[2] << 8) | data_config[3]);
    writeReg(MANG_H, (data_config[4] << 8) | data_config[5]);
    writeReg(CONF_H, (data_config[6] << 8) | data_config[7]);
}

#endif // AS5600_HPP
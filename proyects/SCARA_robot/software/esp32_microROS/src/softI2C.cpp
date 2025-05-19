#include "softI2C.hpp"

void softI2C::begin(uint8_t sda_pin, uint8_t scl_pin, uint32_t SCL_FREQ) {
    pinMode(sda_pin, OUTPUT_OPEN_DRAIN);
    pinMode(scl_pin, OUTPUT_OPEN_DRAIN);
    digitalWrite(sda_pin, HIGH);
    digitalWrite(scl_pin, HIGH);
    clock_frequency = SCL_FREQ; 
}

softI2C::softI2C(uint8_t sda, uint8_t scl) 
    : sda_pin(sda), scl_pin(scl){
}

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

void softI2C::endTransmission() {
    // Stop condition
    digitalWrite(sda_pin, LOW);
    digitalWrite(scl_pin, HIGH);
    delayMicroseconds(2); 
    digitalWrite(sda_pin, HIGH);
    delayMicroseconds(2);
}

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
};

uint8_t softI2C::read() {

    uint8_t data_buyte = Rx_buffer[recived_bytes-1];
    recived_bytes--;

    return data_buyte;
}
#include <Arduino.h>
#include <Wire.h>
#include <Servo.h>

// Configuración del servo
Servo servo;
const int servoPin = 9; // Cambia este pin según tu conexión (pin PWM en Arduino Uno)

// Dirección I2C del dispositivo
const int I2C_ADDRESS = 0x08;

// Variable para almacenar el ángulo recibido
int servoAngle = 0;

// Función para manejar datos recibidos por I2C
void receiveEvent(int bytes) {
  if (Wire.available()) {
    servoAngle = Wire.read(); // Leer el ángulo enviado por el maestro
    servoAngle = constrain(servoAngle, 0, 180); // Limitar el ángulo entre 0 y 180
    servo.write(servoAngle); // Mover el servo al ángulo recibido
  }
}

void setup() {
  // Inicializar el servo
  servo.attach(servoPin);

  // Inicializar I2C como esclavo
  Wire.begin(I2C_ADDRESS);
  Wire.onReceive(receiveEvent); // Configurar la función de recepción

  // Inicializar comunicación serial
  Serial.begin(9600);

  // Posición inicial del servo
  servo.write(180); // Posición inicial en el centro
}

void loop() {
  // Verificar si hay datos disponibles en el puerto serial
  if (Serial.available()) {
    int angle = Serial.parseInt(); // Leer el ángulo enviado por el puerto serial
    if (angle >= 0 && angle <= 180) { // Validar que el ángulo esté en el rango permitido
      servo.write(angle); // Mover el servo al ángulo recibido
      Serial.print("Servo movido a: ");
      Serial.println(angle); // Confirmar el movimiento
    } else {
      Serial.println("Ángulo inválido. Debe estar entre 0 y 180.");
    }
  }
}

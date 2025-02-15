#include <Servo.h>

Servo myservo;

void setup() {
  myservo.attach(9);  // Attach the servo to pin 9
  Serial.begin(9600); // Start serial communication
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the serial command
    if (command == 'r') {  // If the command is 'r'
      myservo.write(90);   // Rotate the servo to 90 degrees
      delay(1000);         // Wait for 1 second
      myservo.write(0);    // Reset the servo to 0 degrees
    }
  }
}

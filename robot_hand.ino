#include <Servo.h>

void setup() {
  // put your setup code here, to run once:
  for (int i = 2; i < 7; i++) {
    pinMode(i, OUTPUT);
  }

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    bool fingers[] = {false , false , false , false , false};
    for (int i = 0; i < 5; i++) {
      fingers[i] = (data[i] == '1');
    }

    for (int i = 2; i < 7; i++) {
      if (fingers[i - 2]) {
        digitalWrite(i, HIGH);
      } else {
        digitalWrite(i , LOW);
      }
    }
  } 
}
  
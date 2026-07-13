#include <Servo.h>


Servo servos[6];
// 순서대로, 엄 검 중 약 소 / 손목
int pins[6] = {3, 5, 6, 9, 10, 11};
bool prev_fingers[5] = {false, false, false, false, false};
bool same;

void setup() {
  
  for (int i = 0; i < 6; i++) {
    servos[i].attach(pins[i]);
  }

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    same = true;
    bool fingers[5];
    
    // 이전 꺼랑 같은지 비교
    for (int i = 0; i < 5; i++) {
      fingers[i] = (data[i] == '1');
      if (prev_fingers[i] != fingers[i]) {
        same = false;
      }
    }
    
    // 같으면 더 연산 안함
    if (same) {
      return;
    }

    // 비교 대상 갱신
    for (int i = 0; i < 5; i++) {
      prev_fingers[i] = fingers[i];
    }

    for (int i = 0; i < 5; i++) {
      servos[i].write(fingers[i] ? 180 : 0);
    }
    delay(20);
  } 
}
  
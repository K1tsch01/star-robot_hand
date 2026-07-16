#include <Servo.h>


Servo servos[6];
// 순서대로, 엄 검 중 약 소 / 손목(NNN) 근데 손목은 쓸지 안쓸지 모르겠음...
int pins[6] = {3, 5, 6, 9, 10, 11};
bool prev_fingers[5] = {false, false, false, false, false};
int rotate_angle = 0;
bool same;

void setup() {
  
  // 서보 모터 전부 활성화
  for (int i = 0; i < 6; i++) {
    servos[i].attach(pins[i]);
  }

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {

    String data = Serial.readStringUntil('\n');

    if (data.length() < 8) {
      return;
    }

    same = true;
    bool fingers[5];
    
    // 이전 꺼랑 같은지 비교
    for (int i = 0; i < 5; i++) {
      fingers[i] = (data[i] == '1');
      if (prev_fingers[i] != fingers[i]) {
        same = false;
      }
    }
    
    /*
    손목 코드인데, 쓸지 안쓸지 모름.... 있으면 멋있긴 하겠다
    rotate_angle = data.substring(5).toInt();   // 5번부터 끝까지 즉 손목 부분 정보.
    servos[5].write(rotate_angle);
    */

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
#include <Servo.h>


Servo servos[6];
// 순서대로, 엄 검 중 약 소 / 손목(NNN) 근데 손목은 쓸지 안쓸지 모르겠음...
int pins[6] = {3, 5, 6, 9, 10, 11};
bool prev_datas[6] = {false, false, false, false, false , false};
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

    if (data.length() != 6) {
      return;
    }

    same = true;
    bool datas[6];
    
    // 이전 꺼랑 같은지 비교
    for (int i = 0; i < 6; i++) {
      datas[i] = (data[i] == '1');
      if (prev_datas[i] != datas[i]) {
        same = false;
      }
    }

    // 같으면 더 연산 안함
    if (same) {
      return;
    }

    // 비교 대상 갱신
    for (int i = 0; i < 6; i++) {
      prev_datas[i] = datas[i];
    }

    for (int i = 0; i < 6; i++) {
      servos[i].write(fingers[i] ? 180 : 0);
    }
    delay(20);
  } 
}
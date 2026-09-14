
#include <Servo.h>

Servo servos[6];

// 0 - 엄지
// 1 - 엄지 관절
// 2 - 검지
// 3 - 중지
// 4 - 약지 / 소지
// 5 - 손목
int pins[6] = {3, 5, 6, 9, 10, 11};

void setup() {
  for (int i = 0; i < 6; i++) {
    servos[i].attach(pins[i]);
  }

  Serial.begin(9600);
}

void loop() {
  if (!Serial.available()) {
    return;
  }

  String data = Serial.readStringUntil('\n');

  // [엄][검][중][약][소][손목]
  if (data.length() != 6) {
    return;
  }

  // 입력 데이터
  bool thumb  = (data[0] == '1');
  bool index  = (data[1] == '1');
  bool middle = (data[2] == '1');
  bool ring   = (data[3] == '1');
  bool pinky  = (data[4] == '1');
  bool wrist  = (data[5] == '1');

  // =================================
  // 서보 제어
  // =================================

  // 엄지 관절
  servos[1].write(thumb ? 180 : 0);

  // 엄지
  servos[0].write(thumb ? 170 : 110);

  // 검지
  servos[2].write(index ? 180 : 0);

  // 중지
  servos[3].write(middle ? 180 : 0);

  // 약지 + 소지
  if (ring && pinky) {
    servos[4].write(180);
  } else {
    servos[4].write(0);
  }

  // 손목
  servos[5].write(wrist ? 180 : 0);
}

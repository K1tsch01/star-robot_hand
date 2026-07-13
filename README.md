# 로봇 손 소프트웨어
Made by STAR, 2026

## 1. 다운로드

1. 오른쪽 **Releases**에서 원하는 버전을 다운로드합니다.
2. ZIP 파일의 압축을 풉니다.
3. 압축을 푼 폴더를 Visual Studio Code로 엽니다.

## 2. 필요한 라이브러리 설치

Visual Studio Code에서 **터미널**을 열고 다음 명령어를 입력합니다.

```bash
pip install mediapipe
pip install pyserial
```

---

## 3. 아두이노 연결

USB 케이블로 아두이노를 컴퓨터에 연결합니다.

---

## 4. COM 포트 설정

`main.py`에서 사용하는 COM 포트를 자신의 환경에 맞게 변경합니다.

예시

```python
ser = serial.Serial("COM3", 9600)
```

`COM3`을 자신의 포트 번호로 변경하세요.

포트 번호는 **장치 관리자 → 포트(COM 및 LPT)** 에서 확인할 수 있습니다.

> **참고**: `Ctrl + F` 를 이용해 위 코드가 사용된 부분을 쉽게 찾아보세요!

---

## 5. 카메라 번호 설정

카메라가 열리지 않는다면

```python
cv2.VideoCapture(0)
```

의 숫자를

```python
0 → 1 → 2
```

처럼 변경해 보세요.

---

## 6. 아두이노 핀 설정

사용한 회로가 다르다면 `.ino` 파일의 서보 핀 번호를 자신의 회로에 맞게 수정하세요.

---

## 7. 실행

Visual Studio Code에서

```bash
python main.py
```

또는 `main.py`를 열고 오른쪽 위 버튼을 눌러 실행하면 됩니다.

---

## 문제 해결(Troubleshooting)

* `ModuleNotFoundError`

  * `pip install ~` 로 시작하는 두 명령어를 다시 실행하세요.

* 카메라가 열리지 않음

  * `VideoCapture()`의 번호를 변경해 보세요.

* 아두이노가 동작하지 않음

  * COM 포트를 확인하세요.

* 손 인식이 잘 안 됨

  * 조명을 밝게 하고 손이 카메라 안에 모두 들어오도록 해 보세요.

---

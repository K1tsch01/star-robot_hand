import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# -------------------------------
# 모델 로드
# -------------------------------

base_options = python.BaseOptions(
    model_asset_path="hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=10
)

detector = vision.HandLandmarker.create_from_options(options)

# -------------------------------
# 웹캠
# -------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

print("ESC를 누르면 종료됩니다.")

# -------------------------------
# 메인 루프
# -------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(image)

    if result.hand_landmarks:

        print("=" * 40)
        print(f"손 개수 : {len(result.hand_landmarks)}")

        for i, hand in enumerate(result.hand_landmarks):

            print(f"\n손 {i+1}")
            for j, landmark in enumerate(hand):

                print(landmark.z)
                if landmark.z < 0.5:
                    print("가깝습니다.")
                #print(
                #    f"{j:2d} : "
                #    f"x={landmark.x:.3f} "
                #    f"y={landmark.y:.3f} "
                #    f"z={landmark.z:.3f}"
                #)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
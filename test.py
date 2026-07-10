import cv2
import mediapipe as mp
import math

from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
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


def dot(v1, v2):
    return (
        v1[0] * v2[0] +
        v1[1] * v2[1] +
        v1[2] * v2[2]
    )


def length(v):
    return math.sqrt(
        v[0] ** 2 +
        v[1] ** 2 +
        v[2] ** 2
    )


def normalize(v):
    l = length(v)

    if l == 0:
        return (0, 0, 0)

    return (
        v[0] / l,
        v[1] / l,
        v[2] / l
    )


def getFSI(
        p1: NormalizedLandmark,
        p2: NormalizedLandmark,
        p3: NormalizedLandmark,
        p4: NormalizedLandmark
):

    # ------------------------
    # 벡터 생성
    # ------------------------

    vec1 = (
        p2.x - p1.x,
        p2.y - p1.y,
        p2.z - p1.z
    )

    vec2 = (
        p3.x - p2.x,
        p3.y - p2.y,
        p3.z - p2.z
    )

    vec3 = (
        p4.x - p3.x,
        p4.y - p3.y,
        p4.z - p3.z
    )

    # ------------------------
    # 정규화
    # ------------------------

    vec1 = normalize(vec1)
    vec2 = normalize(vec2)
    vec3 = normalize(vec3)

    # ------------------------
    # 방향 유사도 계산
    # ------------------------

    score12 = dot(vec1, vec2)
    score23 = dot(vec2, vec3)
    score13 = dot(vec1, vec3)

    # ------------------------
    # 평균 점수
    # ------------------------

    score = (
        score12 +
        score23 +
        score13
    ) / 3

    return score



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
        if len(result.hand_landmarks) > 1:
            print('현재 2개 이상의 손이 감지되었습니다 하나의 손만 감지시켜주세요!')

        else:
            for i, hand in enumerate(result.hand_landmarks):

                print(f"\n손 {i}")
                thumb = getFSI(
                    hand[1],
                    hand[2],
                    hand[3],
                    hand[4]                
                )
                index = getFSI(
                    hand[5],
                    hand[6],
                    hand[7],
                    hand[8]                
                )
                middle = getFSI(
                    hand[9],
                    hand[10],
                    hand[11],
                    hand[12]                
                )
                ring = getFSI(
                    hand[13],
                    hand[14],
                    hand[15],
                    hand[16]                
                )
                pinky = getFSI(
                    hand[17],
                    hand[18],
                    hand[19],
                    hand[20]                
                )
    
                print(f"Thumb = {thumb:.4f}")
                print(f"Index = {index:.4f}")
                print(f"Middle = {middle:.4f}")
                print(f"Ring = {ring:.4f}")
                print(f"Pinky = {pinky:.4f}")

                # for j, landmark in enumerate(hand): 손 마디 별 루프

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
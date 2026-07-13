import cv2
import mediapipe as mp
import math
import serial

from mediapipe.tasks.python.components.containers.landmark import NormalizedLandmark
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# !! 판정 !!
judgement = 0.95
PINKY_JUDGEMENT = 0.03 # 소지 보정 값 (x5)
THUMB_JUDGEMENT = 0.03 # 엄지 보정 값 (x5)



# 모델 로드
base_options = python.BaseOptions(
    model_asset_path="hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=10
)

detector = vision.HandLandmarker.create_from_options(options)

# 웹캠
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

print("ESC를 누르면 종료됩니다.")

# 손가락 판별
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

def is_extended(FSI_SCORE):
    if FSI_SCORE > judgement:
        return True
    else:
        return False

def getFSI(
        p1: NormalizedLandmark,
        p2: NormalizedLandmark,
        p3: NormalizedLandmark,
        p4: NormalizedLandmark
):

    # 벡터 계산
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

    # 정규화
    vec1 = normalize(vec1)
    vec2 = normalize(vec2)
    vec3 = normalize(vec3)

    # 방향 유사도 계산
    score12 = dot(vec1, vec2)
    score23 = dot(vec2, vec3)
    score13 = dot(vec1, vec3)


    # 평균 점수
    score = (
        score12 +
        score23 +
        score13
    ) / 3

    return score

# 아두이노 통신
try:
    ser = serial.Serial("COM9", 9600)
    IS_CONNECTED = True
except:
    IS_CONNECTED = False
    print("아두이노 연결에 실패했습니다. 포트를 확인해주세요.\n카메라 모드로 전환됩니다.")
    
def send(arr: list[bool]):
    DATA = ""
    if len(arr) != 5:
        print("아두이노 통신 함수 오류")
        exit(0)
    else:
        for ar in arr:
            if ar:
                DATA += "1"
            else:
                DATA += "0"
        ser.write((DATA + "\n").encode())

# 메인 루프
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

        # print("=" * 40)
        # print(f"손 개수 : {len(result.hand_landmarks)}")
        if len(result.hand_landmarks) > 1:
            print('현재 2개 이상의 손이 감지되었습니다 하나의 손만 감지시켜주세요!')

            height, width = frame.shape[:2]

            box_w = 500
            box_h = 60

            x1 = (width - box_w) // 2
            y1 = (height - box_h) // 2
            x2 = x1 + box_w
            y2 = y1 + box_h

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), -1)
                                                    
            text = "Two or more hands are detected"

            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 1

            (text_w, text_h), baseline = cv2.getTextSize(
                text, font, font_scale, thickness
            )

            text_x = x1 + (box_w - text_w) // 2
            text_y = y1 + (box_h + text_h) // 2

            cv2.putText(
                frame,
                text,
                (text_x, text_y),
                font,
                font_scale,
                (255, 255, 255),
                thickness,
                cv2.LINE_AA
            )
                        

        else:
            for i, hand in enumerate(result.hand_landmarks):

                # print(f"\n손 {i}")
                
                fingers = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
                fsi_infos = [0.0] * 5
                is_ext = [False] * 5

                for i in range(5):
                    arg = i * 4
                    fsi_infos[i] = getFSI(hand[arg + 1], hand[arg + 2], hand[arg + 3], hand[arg + 4])
                    fsi_infos[0] += THUMB_JUDGEMENT
                    fsi_infos[4] += PINKY_JUDGEMENT # 엄지 / 약지 보정
                    is_ext[i] = fsi_infos[i] >= judgement

                for finger, fsi, ext in zip(fingers, fsi_infos, is_ext):
                    print(f"{finger:6} = {fsi:.4f} {ext}")

                #for iex in is_ext: 해보니까 그냥 억지 연산량만 늘어남
                #    if iex:
                #        print("■", end="")
                #    else:
                #        print("□", end="")

                # 아두이노 전송
                if (IS_CONNECTED):
                    send(is_ext)

                # for j, landmark in enumerate(hand): 손 마디 별 루프

                # 인식 확인하기용 카메라에 등장하는 박스
                lm_boxes = [4, 8, 12, 16, 20]
                height, width = frame.shape[:2]
                for lm in lm_boxes:
                    x = int(hand[lm].x * width)
                    y = int(hand[lm].y * height)
                    j = 0
                    color = [[0, 255, 0], [0, 0, 255]] # GREEN / RED

                    res = ["EXTENDED", "BENT"]
                    if is_ext[int((lm / 4) - 1)]:
                        j = 0
                    else:
                        j = 1

                    (text_w, text_h), baseline = cv2.getTextSize(
                        res[j],
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        1
                    )

                    padding = 5

                    # 박스 위치 (손가락 끝 위쪽)
                    x1 = x - padding
                    y1 = y - text_h - baseline - padding * 2
                    x2 = x + text_w + padding
                    y2 = y

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color[j], 2)
                    cv2.putText(
                        frame,
                        res[j],
                        (x, y - baseline - padding),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        color[j],
                        1
                    )



    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

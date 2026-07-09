import cv2
import mediapipe as mp
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 설정
base_options = python.BaseOptions(
    model_asset_path = "hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options = base_options,
    num_hands = 2
)

detector = vision.HandLandmarker.create_from_options(options)

# 카메라
camera = cv2.VideoCapture(0)

# 메인 로직
while True:
    success, frame = camera.read();
    # frame = 1920 * 1080 * 3 같은 이미지

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image = mp.Image(
        image_format = mp.ImageFormat.SRGB,
        data = rgb
    )

    result = detector.detect(image)

    if result.hand_landmark:
        for hand in result.hand_landmark:
            tip = hand[8]
    else:
        print("There's no hand in camera.")
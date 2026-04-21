import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import urllib.request
import os

MODEL_PATH = "hand_landmarker.task"

if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmarker model...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task",
        MODEL_PATH
    )

CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20),
    (5,9),(9,13),(13,17)
]

class HandDetector:
    def __init__(self, max_hands=2, confidence=0.8):
        base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.latest_result = None
        self.last_landmarks = None

    def find_hands(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        self.latest_result = self.detector.detect(mp_image)

        if self.latest_result.hand_landmarks:
            self.last_landmarks = self.latest_result.hand_landmarks

        return self.latest_result.hand_landmarks

    def draw(self, frame):
        landmarks_to_draw = self.latest_result.hand_landmarks \
            if self.latest_result and self.latest_result.hand_landmarks \
            else self.last_landmarks

        if not landmarks_to_draw:
            return

        h, w = frame.shape[:2]

        is_live = bool(self.latest_result and self.latest_result.hand_landmarks)
        dot_color = (0, 255, 0) if is_live else (0, 165, 255)
        line_color = (255, 255, 255) if is_live else (100, 100, 100)

        for hand in landmarks_to_draw:
            for lm in hand:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 5, dot_color, -1)
            for start_idx, end_idx in CONNECTIONS:
                x1, y1 = int(hand[start_idx].x * w), int(hand[start_idx].y * h)
                x2, y2 = int(hand[end_idx].x * w), int(hand[end_idx].y * h)
                cv2.line(frame, (x1, y1), (x2, y2), line_color, 2)
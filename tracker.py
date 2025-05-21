import cv2
import threading
import numpy as np
import mediapipe as mp

from ursina import Vec3

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

# Landmarks delle mani
hand_landmarks = [[], []]  # [mano0, mano1]
hand_lock = threading.Lock()


def hand_tracking_thread():
    global hand_landmarks
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        result = hands.process(image)

        with hand_lock:
            hand_landmarks = [[], []]
            if result.multi_hand_landmarks:
                for i, hand in enumerate(result.multi_hand_landmarks):
                    if i >= 2:
                        break
                    hand_landmarks[i] = [
                        Vec3(lm.x - 0.5, -lm.y + 0.5, lm.z) * 10 for lm in hand.landmark
                    ]


def start_tracking():
    t = threading.Thread(target=hand_tracking_thread, daemon=True)
    t.start()


def get_hand_positions():
    with hand_lock:
        return hand_landmarks.copy()

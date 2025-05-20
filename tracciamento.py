# tracciamento.py
import cv2
import threading
import numpy as np
import mediapipe as mp
from config import hand_landmarks

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                       min_detection_confidence=0.7, min_tracking_confidence=0.6)

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Compatibilità Linux
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def webcam_loop():
    global hand_landmarks
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        temp = [[], []]
        if results.multi_hand_landmarks:
            for i, hand in enumerate(results.multi_hand_landmarks):
                if i >= 2: break
                for lm in hand.landmark:
                    temp[i].append((lm.x, lm.y, lm.z))
        hand_landmarks[0] = temp[0]
        hand_landmarks[1] = temp[1]
        cv2.waitKey(1)

def start_tracciamento():
    t = threading.Thread(target=webcam_loop, daemon=True)
    t.start()

# 01_tracciamento_mani.py
from ursina import *
import cv2
import threading
import mediapipe as mp

app = Ursina()
window.color = color.black
camera.position = (0, 0, -8)

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                       min_detection_confidence=0.7, min_tracking_confidence=0.6)

cap = cv2.VideoCapture(0)
hand_landmarks = [[], []]  # [mano sinistra, mano destra]

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
                if i >= 2:
                    break
                for lm in hand.landmark:
                    temp[i].append((lm.x, lm.y, lm.z))
        hand_landmarks = temp

threading.Thread(target=webcam_loop, daemon=True).start()

def create_hand_entities(color=color.azure):
    return [Entity(model='sphere', color=color, scale=0.05) for _ in range(21)]

left_hand = create_hand_entities(color.orange)
right_hand = create_hand_entities(color.cyan)

def map_position(x, y, z):
    return Vec3((x - 0.5) * 6, (0.5 - y) * 4, -z * 6)

def update():
    for i, hand in enumerate(hand_landmarks):
        if not hand or len(hand) < 21:
            continue
        entities = left_hand if i == 0 else right_hand
        for j, (x, y, z) in enumerate(hand):
            entities[j].position = map_position(x, y, z)

app.run()

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import cv2
import mediapipe as mp
import numpy as np
import threading

time_index = 0

app = Ursina()
window.title = 'RealInt Lab'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = True
window.fps_counter.enabled = True

# Ambiente laboratorio base
Sky()
lab_floor = Entity(model='plane', scale=(50, 1, 50), texture='white_cube', texture_scale=(50, 50), collider='box', color=color.gray)
walls = [
    Entity(model='cube', scale=(50, 10, 1), position=(0, 5, 25), color=color.gray, collider='box'),
    Entity(model='cube', scale=(50, 10, 1), position=(0, 5, -25), color=color.gray, collider='box'),
    Entity(model='cube', scale=(1, 10, 50), position=(25, 5, 0), color=color.gray, collider='box'),
    Entity(model='cube', scale=(1, 10, 50), position=(-25, 5, 0), color=color.gray, collider='box')
]

# Oggetti interattivi
button = Entity(model='cube', color=color.azure, position=(2, 1, 2), scale=(1, 0.2, 1), collider='box')
grab_object = Entity(model='cube', color=color.orange, position=(0, 1, 0), scale=0.5, collider='box')
grabbed = False

# Controller
player = FirstPersonController()
player.gravity = 0.5
player.jump_height = 1
player.cursor.visible = True

# Rappresentazione mani
hand_entities = []

def create_hand_entities(color=color.red):
    hand = []
    for i in range(21):
        e = Entity(model='sphere', scale=0.1, color=color)
        hand.append(e)
    return hand

left_hand = create_hand_entities(color.green)
right_hand = create_hand_entities(color.red)
hand_entities = [left_hand, right_hand]

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)
landmarks_global = [[], []]

def hand_tracking_loop():
    global landmarks_global
    while True:
        success, frame = cap.read()
        if not success:
            continue
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        landmarks_global = [[], []]
        if result.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                for lm in hand_landmarks.landmark:
                    x = lm.x - 0.5
                    y = -(lm.y - 0.5)
                    z = -lm.z
                    try:
                        landmarks_global[idx].append((x * 10, y * 10 + 2, z * 10))
                    except IndexError as e:
                        #print(f"[Managed Error] { e }")
                        pass

tracking_thread = threading.Thread(target=hand_tracking_loop, daemon=True)
tracking_thread.start()

def update():
    global grabbed

    # Mostra mani
    for hand_idx, hand in enumerate(hand_entities):
        if hand_idx < len(landmarks_global) and landmarks_global[hand_idx]:
            for i, landmark in enumerate(landmarks_global[hand_idx]):
                hand[i].position = Vec3(*landmark)

    # Afferramento base: mano destra indice e pollice vicini
    if len(landmarks_global[1]) >= 9:
        thumb_tip = Vec3(*landmarks_global[1][4])
        index_tip = Vec3(*landmarks_global[1][8])
        dist = distance(thumb_tip, index_tip)

        if dist < 0.3 and not grabbed:
            print(f"{ time_index + 1 } [LOG - Gesture - Right hand] Pinched")
            if distance(grab_object.position, index_tip) < 1:
                grab_object.position = index_tip
                grabbed = True
        elif grabbed:
            if dist > 0.4:
                grabbed = False
            else:
                grab_object.position = index_tip

    # Pulsante premuto se la mano sinistra scende su di esso
    if len(landmarks_global[0]) >= 9:
        left_index_tip = Vec3(*landmarks_global[0][8])
        if distance(button.position, left_index_tip) < 0.5:
            button.color = color.lime
        else:
            button.color = color.azure

app.run()

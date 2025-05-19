from ursina import *
import cv2
import threading
import mediapipe as mp

app = Ursina()
camera.position = (0, 0, -8)
window.color = color.black

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)

cap = cv2.VideoCapture(0)
hand_landmarks = [[], []]  # mano sinistra [0], destra [1]

def webcam_loop():
    global hand_landmarks
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        landmarks = [[], []]
        if results.multi_hand_landmarks:
            for i, hand in enumerate(results.multi_hand_landmarks):
                if i >= 2:
                    break
                for lm in hand.landmark:
                    landmarks[i].append((lm.x, lm.y, lm.z))
        hand_landmarks = landmarks

# Avvia thread webcam
t = threading.Thread(target=webcam_loop, daemon=True)
t.start()

# Costruzione delle mani virtuali
def create_hand_entities(color=color.azure):
    return [Entity(model='sphere', color=color, scale=0.05) for _ in range(21)]

left_hand = create_hand_entities(color.orange)
right_hand = create_hand_entities(color.cyan)

# Oggetti interagibili
objects = []
for i in range(3):
    cube = Draggable(model='cube', color=color.random_color(), scale=0.3, position=(i - 1, -1, 1))
    objects.append(cube)

# Per gestire il grab
grab_threshold = 0.05
held_objects = [None, None]

def is_pinch(hand):
    if len(hand) < 8:
        return False
    thumb_tip = Vec3(*hand[4])
    index_tip = Vec3(*hand[8])
    return distance(thumb_tip, index_tip) < grab_threshold

def map_position(x, y, z):
    # Calibrazione semplice
    x3 = (x - 0.5) * 6
    y3 = (0.5 - y) * 4
    z3 = -z * 5
    return Vec3(x3, y3, z3)

def update():
    for hand_id, landmarks in enumerate(hand_landmarks):
        if not landmarks or len(landmarks) < 21:
            continue

        hand_entities = left_hand if hand_id == 0 else right_hand
        for i, (x, y, z) in enumerate(landmarks):
            pos = map_position(x, y, z)
            hand_entities[i].position = pos

        # Gestione interazione
        pinching = is_pinch(landmarks)
        pinch_pos = map_position(*landmarks[8])

        if pinching and not held_objects[hand_id]:
            for obj in objects:
                if distance(obj.position, pinch_pos) < 0.3:
                    held_objects[hand_id] = obj
                    break
        elif not pinching:
            held_objects[hand_id] = None

        # Aggiorna posizione dell’oggetto afferrato
        if held_objects[hand_id]:
            held_objects[hand_id].position = pinch_pos

app.run()

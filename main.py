from ursina import *
from environment import build_environment
from hand_model import HandModel
from hand_tracker import HandTracker
from physics import setup_physics

app = Ursina()
window.title = 'RealInt - Interactive Lab'
window.borderless = False
window.size = (1280, 720)

# Setup ambiente
build_environment()
setup_physics()

# Inizializza tracciamento e modello mano
tracker = HandTracker()
hand = HandModel()

def update():
    landmarks = tracker.get_hand_landmarks()
    if landmarks:
        hand.update_from_landmarks(landmarks)

app.run()

# interazione_oggetti.py
from ursina import *
import numpy as np

class Afferrabile(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='cube', collider='box', texture='white_cube', scale=0.3,
                         color=color.random_color(), **kwargs)
        self.original_color = self.color
        self.following = False
        self.hand_index = None

    def afferra(self, hand_index):
        self.following = True
        self.hand_index = hand_index
        self.color = color.green

    def rilascia(self):
        self.following = False
        self.hand_index = None
        self.color = self.original_color

    def update_follow(self, landmarks):
        if self.following and landmarks and len(landmarks) > 8:
            x, y, z = landmarks[8]
            self.position = Vec3((x - 0.5) * 6, (0.5 - y) * 4, -z * 6)

def rileva_pinch(landmarks, soglia=0.05):
    if not landmarks or len(landmarks) < 9:
        return False
    p1 = np.array(landmarks[4])
    p2 = np.array(landmarks[8])
    return np.linalg.norm(p1 - p2) < soglia

def crea_oggetti_afferrabili(n=5):
    return [Afferrabile(position=(np.random.uniform(-4, 4), 1.5, np.random.uniform(-4, 4))) for _ in range(n)]

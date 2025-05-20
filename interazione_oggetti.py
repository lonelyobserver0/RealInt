# 03_interazione_oggetti.py
from ursina import *
import numpy as np

class Afferrabile(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='cube', collider='box', texture='white_cube', scale=0.3, color=color.random_color(), **kwargs)
        self.original_color = self.color
        self.following = False
        self.hand_index = None  # 0: sinistra, 1: destra

    def afferra(self, hand_index):
        self.following = True
        self.hand_index = hand_index
        self.color = color.green

    def rilascia(self):
        self.following = False
        self.hand_index = None
        self.color = self.original_color

    def update_follow(self, hand_landmarks):
        if self.following and hand_landmarks and len(hand_landmarks) > 8:
            # MediaPipe landmark 8 = indice, 4 = pollice
            x, y, z = hand_landmarks[8]
            self.position = Vec3((x - 0.5) * 6, (0.5 - y) * 4, -z * 6)


def rileva_pinch(landmarks, soglia=0.05):
    if not landmarks or len(landmarks) < 9:
        return False
    p1 = np.array(landmarks[4])  # pollice
    p2 = np.array(landmarks[8])  # indice
    return np.linalg.norm(p1 - p2) < soglia


def crea_oggetti_afferrabili(n=5):
    oggetti = []
    for i in range(n):
        e = Afferrabile(position=(np.random.uniform(-4, 4), 1.5, np.random.uniform(-4, 4)))
        e.collider = 'box'
        e.collider = BoxCollider(e, center=Vec3(0, 0, 0), size=Vec3(0.3, 0.3, 0.3))
        oggetti.append(e)
    return oggetti

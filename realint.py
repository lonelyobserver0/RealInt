# main.py
from ursina import *
from config import hand_landmarks
from tracciamento import start_tracciamento
from laboratorio import crea_laboratorio
from interazione_oggetti import crea_oggetti_afferrabili, rileva_pinch

app = Ursina()
window.color = color.black
camera.position = (0, 3, -10)


def map_position(x, y, z):
    return Vec3((x - 0.5) * 6, (0.5 - y) * 4, -z * 6)


start_tracciamento()
crea_laboratorio()
oggetti = crea_oggetti_afferrabili()


def update():
    for obj in oggetti:
        idx = obj.hand_index
        if idx is not None:
            obj.update_follow(hand_landmarks[idx])

    for i, hand in enumerate(hand_landmarks):
        if not hand:
            continue
        if rileva_pinch(hand):
            for obj in oggetti:
                if not obj.following and distance(obj.position, map_position(*hand[8])) < 0.3:
                    obj.afferra(i)
        else:
            for obj in oggetti:
                if obj.hand_index == i:
                    obj.rilascia()


app.run()

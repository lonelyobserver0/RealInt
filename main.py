from ursina import *
from physics import setup_physics, step_physics
from lab_scene import load_lab_scene
from tracker import start_tracking, get_hand_positions

start_tracking()

hand_spheres = [Entity(model='sphere', color=color.red, scale=0.1) for _ in range(21)]
hand2_spheres = [Entity(model='sphere', color=color.green, scale=0.1) for _ in range(21)]

def update():
    step_physics(time.dt)

    hands = get_hand_positions()
    if hands[0]:
        for i, pos in enumerate(hands[0]):
            hand_spheres[i].position = pos
    if hands[1]:
        for i, pos in enumerate(hands[1]):
            hand2_spheres[i].position = pos

app = Ursina()

setup_physics()
load_lab_scene()

camera.position = (0, 10, -20)
camera.rotation_x = 20

def update():
    step_physics(time.dt)

app.run()

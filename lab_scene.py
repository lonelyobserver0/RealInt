from ursina import *
from objects import create_box

def load_lab_scene():
    floor = Entity(model='plane', scale=(50, 1, 50), color=color.gray, position=(0, 0, 0), collider='box')
    wall1 = Entity(model='cube', scale=(1, 5, 20), color=color.light_gray, position=(-25, 2.5, 0), collider='box')
    wall2 = Entity(model='cube', scale=(1, 5, 20), color=color.light_gray, position=(25, 2.5, 0), collider='box')
    table = create_box(position=(0, 1, 0), size=(2, 0.5))
    box1 = create_box(position=(-2, 3, 0))
    box2 = create_box(position=(2, 5, 0))

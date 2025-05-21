from ursina import *
from physics import add_physics_box

def create_box(position=(0, 5, 0), color=color.orange, size=(1, 1)):
    box = Entity(model='cube', color=color, scale=(size[0], size[1], 1), position=position, collider='box')
    add_physics_box(box, size=size)
    return box

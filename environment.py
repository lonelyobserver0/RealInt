from ursina import *


def build_environment():
    Sky()
    ground = Entity(model='plane', scale=(50, 1, 50), collider='box', texture='white_cube', texture_scale=(50, 50),
                    color=color.gray)

    # Oggetti da laboratorio
    Entity(model='cube', color=color.azure, position=(2, 0.5, 2), scale=1, collider='box')
    Entity(model='cube', color=color.red, position=(-2, 0.5, 1), scale=(1, 2, 1), collider='box')
    Entity(model='cube', color=color.green, position=(0, 0.5, -3), scale=(1, 1, 2), collider='box')

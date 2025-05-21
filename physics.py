from ursina import *
from ursina.physics import *

def setup_physics():
    # Aggiunge fisica globale
    gravity = 9.81
    Entity(model='sphere', color=color.yellow, position=(0,5,0), scale=0.5, collider='sphere', gravity=gravity)
    Entity(model='cube', color=color.orange, position=(-3,3,1), scale=0.7, collider='box', gravity=gravity)

# laboratorio.py
from ursina import *

def crea_laboratorio():
    floor = Entity(model='plane', scale=20, texture='white_cube', texture_scale=(10,10), collider='box')
    pareti = [
        Entity(model='cube', scale=(20,10,0.2), position=(0,5,10), color=color.gray, collider='box'),
        Entity(model='cube', scale=(0.2,10,20), position=(10,5,0), color=color.gray, collider='box'),
        Entity(model='cube', scale=(0.2,10,20), position=(-10,5,0), color=color.gray, collider='box'),
        Entity(model='cube', scale=(20,10,0.2), position=(0,5,-10), color=color.gray, collider='box'),
    ]
    luci = [
        PointLight(parent=camera, color=color.white, position=(0,10,-5)),
        AmbientLight(color=color.rgba(100,100,100,0.4))
    ]

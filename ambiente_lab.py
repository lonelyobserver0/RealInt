# Module 02: ambiente_lab.py
from ursina import *

def crea_laboratorio():
    # Pavimento
    pavimento = Entity(model='plane', scale=(20, 1, 20), collider='box', texture='white_cube', texture_scale=(10,10), color=color.gray)

    # Pareti
    pareti = [
        Entity(model='cube', position=(0, 5, 10), scale=(20, 10, 1), collider='box', color=color.light_gray),  # dietro
        Entity(model='cube', position=(0, 5, -10), scale=(20, 10, 1), collider='box', color=color.light_gray), # davanti
        Entity(model='cube', position=(10, 5, 0), scale=(1, 10, 20), collider='box', color=color.light_gray),  # destra
        Entity(model='cube', position=(-10, 5, 0), scale=(1, 10, 20), collider='box', color=color.light_gray), # sinistra
        Entity(model='cube', position=(0, 10, 0), scale=(20, 1, 20), collider='box', color=color.light_gray),  # soffitto
    ]

    # Banco da lavoro
    banco = Entity(model='cube', position=(0, 1, 0), scale=(6, 1, 2), collider='box', color=color.brown)

    # Mensole
    mensola1 = Entity(model='cube', position=(-5, 3, -4), scale=(4, 0.2, 1), color=color.gray)
    mensola2 = Entity(model='cube', position=(5, 3, -4), scale=(4, 0.2, 1), color=color.gray)

    # Porta (finta per ora)
    porta = Entity(model='cube', position=(0, 5, -9.5), scale=(3, 7, 0.5), collider='box', color=color.rgb(100,100,150))

    # Illuminazione
    Sky()
    DirectionalLight(y=2, z=3, shadows=True)

    print("✅ Laboratorio creato.")

# ESEMPIO: se esegui direttamente questo modulo
if __name__ == '__main__':
    app = Ursina()
    crea_laboratorio()
    app.run()

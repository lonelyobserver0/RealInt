from ursina import *

class HandModel(Entity):
    def __init__(self):
        super().__init__()
        self.joints = [Entity(model='sphere', scale=0.02, color=color.orange) for _ in range(21)]

    def update_from_landmarks(self, landmarks):
        for i, lm in enumerate(landmarks):
            self.joints[i].position = Vec3(lm.x - 0.5, -lm.y + 0.5, -lm.z)

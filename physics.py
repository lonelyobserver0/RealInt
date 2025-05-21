import pymunk

space = pymunk.Space()
space.gravity = (0, -1500)

# Mappa tra body pymunk e entità Ursina
physics_entities = []

def setup_physics():
    static_body = space.static_body
    floor = pymunk.Segment(static_body, (-1000, 0), (1000, 0), 5)
    floor.friction = 1.0
    space.add(floor)

def add_physics_box(entity, size=(1,1), mass=1):
    width, height = size
    moment = pymunk.moment_for_box(mass, (width * 100, height * 100))
    body = pymunk.Body(mass, moment)
    body.position = entity.x * 100, entity.y * 100

    shape = pymunk.Poly.create_box(body, (width * 100, height * 100))
    shape.friction = 0.8

    space.add(body, shape)
    physics_entities.append((entity, body))

def step_physics(dt):
    space.step(dt)
    for entity, body in physics_entities:
        entity.x = body.position.x / 100
        entity.y = body.position.y / 100

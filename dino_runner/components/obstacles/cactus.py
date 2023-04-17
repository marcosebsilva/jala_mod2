import random

from dino_runner.components.obstacles.obstacle import Obstacle

class Cactus(Obstacle):
    def __init__(self, image, rect_y = 325):
        self.type = random.randint(0, len(image) - 1)
        super().__init__(image, self.type)
        # this allows us to have different sized cactus
        # the bad thing is that we have to directly set a Y value.
        # i should probably make a better way to do this
        self.rect.y = rect_y
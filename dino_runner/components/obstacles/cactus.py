import random

from dino_runner.components.obstacles.obstacle import Obstacle

class Cactus(Obstacle):
    def __init__(self, image, rect_y = 325):
        random_type = random.randint(0, len(image) - 1)
        super().__init__(image, random_type)
        self.rect.y = rect_y
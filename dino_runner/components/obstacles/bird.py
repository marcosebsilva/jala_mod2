from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

class Bird(Obstacle):
    def __init__(self):
        super().__init__(BIRD, 0)
        self.rect.y = 100
        self.step_index = 0

    def draw(self, screen):
        image = self.image[0] if self.step_index < 5 else self.image[1]

        screen.blit(image, (self.rect.x, self.rect.y))

        self.step_index += 1
        if self.step_index > 10:
            self.step_index = 0

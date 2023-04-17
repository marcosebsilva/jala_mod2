from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

class Bird(Obstacle):
    def __init__(self):
        super().__init__(BIRD, 0)
        self.rect.y = 100
        self.step_index = 0

    def fly(self):
        self.type = 0 if self.step_index < 5 else 1
        self.step_index += 1

    def update(self, game_speed, obstacles):
        super().update(game_speed, obstacles)
        self.fly()

        if self.step_index > 10:
            self.step_index = 0

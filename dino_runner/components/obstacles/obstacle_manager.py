import random
from typing import List

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS

class ObstacleManager:
    obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            obstacle_options = [
                Cactus(SMALL_CACTUS),
                Cactus(LARGE_CACTUS, 300),
                Bird()
            ]
            self.obstacles.append(random.choice(obstacle_options))


        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                game.death_count += 1
                game.playing = False
                break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def clear_obstacles(self):
        self.obstacles.clear()
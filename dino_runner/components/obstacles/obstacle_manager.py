import random
import pygame

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

from dino_runner.utils.constants import SMALL_CACTUS, DEFAULT_TYPE, LARGE_CACTUS, DEAD_DINO

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
                if not game.player.has_power_up:
                    game.death_count += 1
                    game.playing = False
                    break
                elif game.player.shield:
                    self.obstacles.remove(obstacle)
                    game.player.shield = False
                    game.player.type = DEFAULT_TYPE
                    game.player.has_power_up = False
                elif game.player.hammer:
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def clear_obstacles(self):
        self.obstacles.clear()
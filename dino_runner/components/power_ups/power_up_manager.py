import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.utils.constants import DEFAULT_TYPE, SHIELD, SHIELD_TYPE, SCREEN_HEIGHT, SCREEN_WIDTH, HAMMER_TYPE
from dino_runner.utils.text_helpers import draw_text


class PowerUpManager:
    power_ups = []
    when_appears = 200
    power_up_options = [Shield, Hammer]

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears = score + random.randint(400, 500)
            self.power_ups.append(random.choice(self.power_up_options)())

    def toggle_powers(self, player, power_up):
        player.has_power_up = True
        player.power_up_time = power_up.start_time + (power_up.duration * 1000)
        player.type = power_up.type
    
        if player.type == SHIELD_TYPE:
            player.hammer = False
            player.shield = True
        elif player.type == HAMMER_TYPE:
            player.shield = False
            player.hammer = True

    def update(self,score, game_speed, player):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):                    
                power_up.start_time = pygame.time.get_ticks()
                self.toggle_powers(player, power_up)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def clear_power_ups(self):
        self.power_ups.clear()
        self.when_appears = 0
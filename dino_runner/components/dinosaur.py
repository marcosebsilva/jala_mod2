import pygame
from dino_runner.utils.constants import RUNNING, RUNNING_HAMMER, DUCKING_HAMMER, JUMPING_HAMMER, JUMPING, DUCKING, DEFAULT_TYPE, SHIELD_TYPE, DUCKING_SHIELD, JUMPING_SHIELD, RUNNING_SHIELD, HAMMER_TYPE, HAMMER
from pygame.sprite import Sprite


RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}
DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}

DEFAULT_X_POS = 80
DEFAULT_Y_POS = 310
DEFAULT_JUMP_VEL = 8.5
class Dinosaur(Sprite):
    type = DEFAULT_TYPE
    image = RUN_IMG[DEFAULT_TYPE][0]
    dino_rect = image.get_rect()
    dino_rect.x = DEFAULT_X_POS
    dino_rect.y = DEFAULT_Y_POS
    step_index = 0
    power_up_time = 0
    running = True 
    jumping = False
    jump_vel = DEFAULT_JUMP_VEL
    ducking = False
    has_power_up = False
    shield = False
    remaining_power_time = 0
    hammer = False
    show_text = False
    shield_time_up = 0

    def update(self, user_input):
        if self.running:
            self.run()
        elif self.jumping:
            self.jump()
        elif self.ducking:
            self.duck()
    
        if self.step_index >= 9:
            self.step_index = 0

        if user_input[pygame.K_UP] and not self.jumping:
            self.jumping = True
            self.running = False
        elif user_input[pygame.K_DOWN] and not self.jumping:
            self.ducking = True
            self.running = False
        elif not self.jumping:
            self.running = True
            self.jumping = False

    def run(self):
        self.image = RUN_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = DEFAULT_X_POS
        self.dino_rect.y = DEFAULT_Y_POS
        self.step_index += 1

    def reset(self):
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = DEFAULT_X_POS
        self.dino_rect.y = DEFAULT_Y_POS
        self.step_index = 0
        self.type = DEFAULT_TYPE
        self.running = True 
        self.jumping = False
        self.jump_vel = DEFAULT_JUMP_VEL
        self.ducking = False

    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = DEFAULT_X_POS
        self.dino_rect.y = DEFAULT_Y_POS + (self.dino_rect.height // 2) #this is assuming the ducking image is half the size of the running image
        self.step_index += 1

    def jump(self):
        self.image = JUMP_IMG[self.type]
        if self.jumping:
            self.dino_rect.y -= int(self.jump_vel * 4)
            self.jump_vel -= 0.8

        if self.jump_vel < -DEFAULT_JUMP_VEL:
            self.dino_rect.y = DEFAULT_Y_POS
            self.jumping = False
            self.jump_vel = DEFAULT_JUMP_VEL

    def draw(self, screen: pygame.Surface):
        if not self.hammer:
            screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        elif self.remaining_power_time <= 2:
            print(self.power_up_time)
            if(pygame.time.get_ticks() % 2 == 0):
                screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        else:
            screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

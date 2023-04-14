import pygame
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING
from pygame.sprite import Sprite

class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self):
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.running = True 
        self.jumping = False
        self.jump_vel = self.JUMP_VEL
        self.ducking = False
        

    # this doesn't seem to scale well
    # probably should have a list of states and a current state or some kind of event system
    def update(self, user_input):
        if self.running:
            self.run()
        elif self.jumping:
            self.jump()
        elif self.ducking:
            self.duck()
    
        if self.step_index >= 10:
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
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = DUCKING[0] if self.step_index < 5 else DUCKING[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS + (self.dino_rect.height // 2) #this is assuming the ducking image is half the size of the running image
        self.step_index += 1

    def jump(self):
        self.image = JUMPING
        if self.jumping:
            self.dino_rect.y -= int(self.jump_vel * 4)
            self.jump_vel -= 0.8

        if self.jump_vel < -self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.jumping = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
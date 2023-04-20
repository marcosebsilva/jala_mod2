import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, SHIELD, GAME_OVER, DEAD_DINO
from dino_runner.utils.text_helpers import draw_text
from dino_runner.components.dinosaur import Dinosaur

from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


FONT_STYLE = "freesansbold.ttf"
DEFAULT_GAME_SPEED = 20
class Game:
    playing = False
    running = False
    game_speed = DEFAULT_GAME_SPEED
    x_pos_bg = 0
    y_pos_bg = 380
    high_score = 0
    score = 0
    death_count = 0
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True

        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def reset(self):
        self.game_speed = DEFAULT_GAME_SPEED
        self.player.reset()
        self.obstacle_manager.clear_obstacles()
        self.power_up_manager.clear_power_ups()

        self.score = 0

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        death_count_message = f"You died {self.death_count} {'time' if self.death_count == 1 else 'times'}!" 

        if self.death_count == 0:
            draw_text(self.screen,"Press any key to start", 22, half_screen_width, half_screen_height)
        else:
            self.screen.blit(GAME_OVER, (half_screen_width - 200, half_screen_height - 140))
            self.screen.blit(DEAD_DINO, (half_screen_width - 40, half_screen_height - 70))

            draw_text(self.screen,f"Your score was: {self.score}.", 18, half_screen_width, half_screen_height + 50)
            if(self.score >= self.high_score):
                self.high_score = self.score
                draw_text(self.screen,f"New high score!", 18, half_screen_width, half_screen_height + 85)
            else:
                draw_text(self.screen,f"Your high score is: {self.high_score}.", 18, half_screen_width, half_screen_height + 85)

            draw_text(self.screen,death_count_message, 18, half_screen_width, half_screen_height + 130)
            draw_text(self.screen,"Press any key to restart.", 18, half_screen_width, half_screen_height + 200)

        pygame.display.update()
        self.handle_menu_events()

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def run(self):
        self.reset()
        # Game loop: events - update - draw
        for i in range(3, 0, -1):
            self.screen.fill((255, 255, 255))
            draw_text(self.screen,str(i), 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.display.update()
            pygame.time.delay(1000)

        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 2

    def update(self):
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.score, self.game_speed, self.player)

        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.update_score()

    def draw_feedback(self):
        if self.player.has_power_up:
            if self.player.hammer:
                time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000)
                if time_to_show >= 0:
                    self.player.remaining_power_time = time_to_show
                    draw_text(self.screen,f"YOU ARE EMPOWERED FOR {time_to_show} SECONDS!", 15, SCREEN_WIDTH // 2, 100)

                else:
                    self.player.has_power_up = False
                    self.player.type = DEFAULT_TYPE
                    self.player.hammer = False
            elif self.player.shield:
                self.screen.blit(SHIELD, (SCREEN_WIDTH // 2, 40))
                draw_text(self.screen,f"SHIELD ACTIVATED!", 15, SCREEN_WIDTH // 2, 20)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background()
        draw_text(self.screen,f"HIGH SCORE: {self.high_score}", 15, 120, 50)
        draw_text(self.screen,f"SCORE: {self.score}", 15, 1000, 50)
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_feedback()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

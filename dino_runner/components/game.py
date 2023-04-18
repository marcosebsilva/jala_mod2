import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.dinosaur import Dinosaur

from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

FONT_STYLE = "freesansbold.ttf"
class Game:
    DEFAULT_GAME_SPEED = 20
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = self.DEFAULT_GAME_SPEED
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.player = Dinosaur()
        self.death_count = 0
        self.obstacle_manager = ObstacleManager()

    def execute(self):
        self.running = True

        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(FONT_STYLE, size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def reset(self):
        self.game_speed = self.DEFAULT_GAME_SPEED
        self.player.reset()
        self.obstacle_manager.clear_obstacles()
        self.score = 0

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        death_count_message = f"You died {self.death_count} {'time' if self.death_count == 1 else 'times'}!" 

        if self.death_count == 0:
            self.draw_text("Press any key to start", 22, half_screen_width, half_screen_height)
        else:
            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))
            self.draw_text(f"Your score was: {self.score}.", 22, half_screen_width, half_screen_height)
            self.draw_text(death_count_message, 22, half_screen_width, half_screen_height + 50)
            self.draw_text("Press any key to restart.", 22, half_screen_width, half_screen_height + 100)

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
            self.draw_text(str(i), 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
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
            self.game_speed += 5

    def update(self):
        self.obstacle_manager.update(self)
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.update_score()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background()
        self.draw_text(f"Score: {self.score}", 22, 1000, 50)
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
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

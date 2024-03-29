import pygame
FONT_STYLE = "freesansbold.ttf"

def draw_text(screen, text: str, size: int, x: int, y: int):
    font = pygame.font.Font('dino_runner/assets/Fonts/press_start_2p.ttf', size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
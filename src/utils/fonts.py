import pygame


def create_text(text, size, color, background_color=None):
    font = pygame.font.Font(None, size)
    return font.render(text, True, color, background_color)

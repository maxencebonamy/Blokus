import pygame
from utils.colors import Colors
from utils.fonts import create_text


class ScoreLabel:

    def __init__(self, color, score):
        self.color = color
        self.score = score

        self.text = create_text(f"Score : {score}", 36, Colors.WHITE.value)
        self.rect = self.text.get_rect()
        self.rect.centerx = self.text.get_rect().centerx
        self.rect.centery = self.text.get_rect().centery
        self.rect.x -= 10
        self.rect.y -= 5
        self.rect.width += 20
        self.rect.height += 10

    def draw(self, screen, center_x, center_y):
        x = center_x - self.rect.width // 2
        y = center_y - self.rect.height // 2
        pygame.draw.rect(screen, self.color, self.rect.move(x, y), 0, 4)
        screen.blit(self.text, (x, y))

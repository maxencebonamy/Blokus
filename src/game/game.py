import pygame
from utils.colors import Colors
from utils.fonts import create_text


class Game:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))

        self.text = create_text("Hello, World!", 36, Colors.BLACK.value)

        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.screen.get_rect().centerx
        self.text_rect.centery = self.screen.get_rect().centery

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(Colors.WHITE.value)
            self.screen.blit(self.text, self.text_rect)

            pygame.display.flip()

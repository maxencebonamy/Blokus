import pygame


class Game:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))

        BLACK = (0, 0, 0)

        font = pygame.font.Font(None, 36)
        self.text = font.render("Hello, World!", True, BLACK)

        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.screen.get_rect().centerx
        self.text_rect.centery = self.screen.get_rect().centery

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.text, self.text_rect)

            pygame.display.flip()

import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)
text = font.render("Hello, World!", True, BLACK)

text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill((255, 255, 255))
	screen.blit(text, text_rect)

	pygame.display.flip()

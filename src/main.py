import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Labyrinthe")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((30, 30, 40))      # fond RGB
    pygame.display.flip()          # affiche l'image

    clock.tick(60)                 # limite à 60 FPS

pygame.quit()
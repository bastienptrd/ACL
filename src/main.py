import pygame
from model.Player import Player
from controller import gameController
import config

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Labyrinthe")
clock = pygame.time.Clock()
player = Player("Player", 100, 200, (400, 300), config.player_img_path)
player_img = player.generate_image()

running = True
while running:
    #print(str(clock.get_fps())) #get current fps
    dt = clock.tick(60) / 1000.0  # Temps écoulé depuis la dernière frame en secondes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.display.flip()
    gameController.player_mouvement(dt,player)
    
    screen.fill((30, 30, 40))          # 1. effacer
    screen.blit(player_img, player.position)  # 2. dessiner
    pygame.display.flip()              # 3. affiche

pygame.quit()
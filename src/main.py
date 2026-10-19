import pygame
from model.Player import Player
import config

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Labyrinthe")
clock = pygame.time.Clock()
player = Player("Player", 100, 200, (400, 300), config.player_img_path)
player_img = pygame.image.load(player.image_path).convert_alpha()
player_img = pygame.transform.scale(player_img, (player_img.get_width()/15, player_img.get_height()/15))  # Redimensionner l'image du joueur à 50x50 pixels
running = True
while running:
    #print(str(clock.get_fps())) #get current fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.display.flip()          

    dt = clock.tick(60) / 1000.0  # Temps écoulé depuis la dernière frame en secondes
    if pygame.key.get_pressed()[pygame.K_UP]:
        player.move("up", player.speed, dt)
    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        player.move("down", player.speed, dt)
    elif pygame.key.get_pressed()[pygame.K_LEFT]:
        player.move("left", player.speed, dt)
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        player.move("right", player.speed, dt)
    print(player.position)
    screen.fill((30, 30, 40))          # 1. effacer
    screen.blit(player_img, player.position)  # 2. dessiner
    pygame.display.flip()              # 3. affiche
pygame.quit()
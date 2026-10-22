from model.Player import Player
import pygame



def player_mouvement(dt,player) :
    if pygame.key.get_pressed()[pygame.K_UP]:
        player.move("up", player.speed, dt)
    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        player.move("down", player.speed, dt)
    elif pygame.key.get_pressed()[pygame.K_LEFT]:
        player.move("left", player.speed, dt)
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        player.move("right", player.speed, dt)


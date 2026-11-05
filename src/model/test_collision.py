"""
Fichier de test réalisé avec l'aide d'une IA.

Sert uniquement à tester la classe Collisions (Collision.py).
Il reprend le vrai labyrinthe généré par la classe Maze (model/maze.py),
mais tout le reste est une version de test très simple :
une fenêtre pygame basique, un dessin simple des cases
et un carré bleu déplacé avec les flèches à la place du joueur.

Ce n'est pas le vrai système de déplacement ni le vrai affichage du jeu.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
import config
from model.maze import Maze
from model.Collision import Collisions

TAILLE_CASE = 40

labyrinthe = Maze(21, 15)
labyrinthe.creerLabyrinthe()
grille = labyrinthe.grille
tailleX, tailleY = labyrinthe.recupTaille()

collisions = Collisions()
collisions.murs_depuis_grille(grille, TAILLE_CASE)

pygame.init()
ecran = pygame.display.set_mode((tailleX * TAILLE_CASE, tailleY * TAILLE_CASE))
pygame.display.set_caption("Test collisions")
horloge = pygame.time.Clock()

joueur = pygame.Rect(TAILLE_CASE + 10, TAILLE_CASE + 10, 20, 20)
vitesse = 4

en_cours = True
while en_cours:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

    touches = pygame.key.get_pressed()
    dx = (touches[pygame.K_RIGHT] - touches[pygame.K_LEFT]) * vitesse
    dy = (touches[pygame.K_DOWN] - touches[pygame.K_UP]) * vitesse
    collisions.deplacer(joueur, dx, dy)

    ecran.fill((255, 255, 255))
    for x in range(tailleX):
        for y in range(tailleY):
            case = pygame.Rect(x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            if grille[x][y] == config.caseMur:
                pygame.draw.rect(ecran, (0, 0, 0), case)
            elif grille[x][y] == config.debut:
                pygame.draw.rect(ecran, (0, 200, 0), case)
            elif grille[x][y] == config.fin:
                pygame.draw.rect(ecran, (200, 0, 0), case)
    pygame.draw.rect(ecran, (0, 0, 255), joueur)

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
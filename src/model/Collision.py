import pygame
import config

class Collisions:
    def __init__(self, murs=None):
        if murs is None:
            murs = []
        self.murs = murs

    def murs_depuis_grille(self, grille, taille_case):
        self.murs = []
        for x in range(len(grille)):
            for y in range(len(grille[x])):
                if grille[x][y] == config.caseMur or grille[x][y] == config.caseObstacle:
                    self.murs.append(pygame.Rect(x * taille_case[0], y * taille_case[1], taille_case[0], taille_case[1]))

    def touche_un_mur(self, joueur_rect):
        for mur in self.murs:
            if joueur_rect.colliderect(mur):
                return True
        return False

    def deplacer(self, joueur_rect, dx, dy):
        joueur_rect.x += dx
        for mur in self.murs:
            if joueur_rect.colliderect(mur):
                if dx > 0:
                    joueur_rect.right = mur.left
                elif dx < 0:
                    joueur_rect.left = mur.right

        joueur_rect.y += dy
        for mur in self.murs:
            if joueur_rect.colliderect(mur):
                if dy > 0:
                    joueur_rect.bottom = mur.top
                elif dy < 0:
                    joueur_rect.top = mur.bottom
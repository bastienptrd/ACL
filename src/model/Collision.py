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
                if grille[x][y] == config.caseMur or grille[x][y] == config.obstacle:
                    self.murs.append(pygame.Rect(x * taille_case, y * taille_case, taille_case, taille_case))

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


if __name__ == "__main__":
    grille = [
        [-1, -1, -1, -1],
        [-1, 0, 0, -1],
        [-1, 0, -1, -1],
        [-1, -1, -1, -1],
    ]
    collisions = Collisions()
    collisions.murs_depuis_grille(grille, 40)

    joueur = pygame.Rect(45, 45, 20, 20)
    for i in range(20):
        collisions.deplacer(joueur, 7, 0)
    print(joueur.x)
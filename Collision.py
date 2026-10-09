import pygame

class Collisions:
    def __init__(self, murs):

        self.murs = murs

    def touche_un_mur(self, joueur_rect):
        for mur in self.murs:
            if joueur_rect.colliderect(mur):
                return True
        return False
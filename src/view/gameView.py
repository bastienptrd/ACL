import pygame


couleurTexte = (240, 240, 240)

class GameView:
    def __init__(self, screen, fondView, grille):
        self.__screen = screen
        self.__fondView = fondView
        # def de la grille pour le labyrinthe
        self.__grille = grille
        self.__tailleCase = 40
        self.__couleurs = {
            0: (60, 90, 60),
            1: (240, 90, 90),
        }

    def dessiner(self):
        largeur, hauteur = self.__screen.get_size()
        self.__screen.fill((0, 0, 0))

        # On dessine la grille en la centrant selon la taille de la fenetre
        nbLignes = len(self.__grille)
        nbColonnes = len(self.__grille[0])
        largeurGrille = nbColonnes * self.__tailleCase
        hauteurGrille = nbLignes * self.__tailleCase

        decalageX = (largeur - largeurGrille) // 2
        decalageY = (hauteur - hauteurGrille) // 2

        for i, ligne in enumerate(self.__grille):
            for j, valeur in enumerate(ligne):
                rect = pygame.Rect(
                    decalageX + j * self.__tailleCase,
                    decalageY + i * self.__tailleCase,
                    self.__tailleCase,
                    self.__tailleCase,
                )
                pygame.draw.rect(self.__screen, self.__couleurs[valeur], rect)
                pygame.draw.rect(self.__screen, (30, 50, 30), rect, width=1)

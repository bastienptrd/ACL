import pygame
import config
import math
from model.Character import Character
from model.Bullet import Bullet

class GameView:
    def __init__(self, screen : pygame.surface.Surface, grille : list[list[int]], position : pygame.Vector2 = (0, 0), tailleRenduCase  : tuple[float, float] = (100, 100)):
        """
        :param screen: fenêtre du jeu
        :param grille: grille généré par le labyrinthe
        :param position: position de la caméra dans le labyrinthe
        :param tailleRenduCase: échelle pour le rendu (taille des case en pixel)
        """

        self.__screen = screen
        self.__tailleRenduCase = tailleRenduCase

        # Grille du labyrinthe
        self.__grille = grille
        # Position du rendu
        self.__position = pygame.Vector2(position)

        # Changer les images du labyrinthe ici config.imagesMurs1 ...
        surf1 = pygame.surface.Surface((100, 100))
        surf1.fill((255, 0, 0))
        surf2 = pygame.surface.Surface((100, 100))
        surf2.fill((0, 255, 0))
        surf3 = pygame.surface.Surface((100, 100))
        surf3.fill((255, 255, 0))
        surf4 = pygame.surface.Surface((100, 100))
        surf4.fill((0, 200, 0))
        surf5 = pygame.surface.Surface((100, 100))
        surf5.fill((200, 0, 0))

        self.__imagesCaseLabyrinthe = {config.caseVide : surf1,
                                       config.caseMur : surf2,
                                       config.caseDebut : surf3,
                                       config.caseFin : surf3,
                                       config.caseObstacle : surf4,
                                       config.caseApparitionEnemi : surf5}

        self.remiseEchelle()

        imageBarre = pygame.image.load(config.barre_vie_images).convert()
        ratio = imageBarre.get_height() / imageBarre.get_width()
        imageBarre = pygame.transform.scale(
            imageBarre,
            (config.barreVieLargeur, int(config.barreVieLargeur * ratio))
        )
        imageBarre.set_colorkey((63, 72, 204))
        self.__imagesBarreVie = imageBarre



    def remiseEchelle(self) -> None:
        """
        Remet les images des murs à l'échelle choisie
        """
        for key, value in self.__imagesCaseLabyrinthe.items():
            self.__imagesCaseLabyrinthe[key] = pygame.transform.scale(value, self.__tailleRenduCase)

    def changePosition(self, position : pygame.Vector2) -> None:
        """
        :param position: Nouvelle position de la caméra
        """
        self.__position = pygame.Vector2(position)

    def recupererPosition(self) -> pygame.Vector2:
        return pygame.Vector2(self.__position)

    def changeGrille(self, grille : list[list[int]]) -> None:
        """
        :param grille: Nouvelle grille
        """
        self.__grille = grille

    def recupererGrille(self) -> list[list[int]]:
        return self.__grille

    def convertirCoordNumVersEcran(self, coord : pygame.Vector2) -> tuple[int, int]:
        """
        :param coord: Coordonnées d'un point du labyrinthe
        :return: Coordonnées correspondantes sur l'écran
        """
        screenLongueur, screenLargeur = self.__screen.get_size()
        positionEcranX = int(screenLongueur / 2 + (coord[0] - self.__position[0]) * (self.__tailleRenduCase[0] - 2))
        positionEcranY = int(screenLargeur / 2 + (coord[1] - self.__position[1]) * (self.__tailleRenduCase[1] - 2))
        return positionEcranX, positionEcranY

    def convertirCoordEcranVersNum(self, coord : tuple[int, int]) -> pygame.Vector2:
        """
        :param coord: Coordonnées d'un point de l'écran
        :return: Coordonnées correspondantes dans le labyrinthe
        """
        screenLongueur, screenLargeur = self.__screen.get_size()
        positionNumX = (coord[0] - screenLongueur / 2) / (self.__tailleRenduCase[0] - 2) + self.__position[0]
        positionNumY = (coord[1] - screenLargeur / 2) / (self.__tailleRenduCase[1] - 2) + self.__position[1]
        return pygame.Vector2(positionNumX, positionNumY)

    def dessinerGrille(self) -> None:
        self.__screen.fill((0, 0, 0))

        for i in range(len(self.__grille)):
            for j in range(len(self.__grille[0])):
                self.__screen.blit(self.__imagesCaseLabyrinthe[self.__grille[i][j]], self.convertirCoordNumVersEcran((i, j)))

    def dessinerCharacter(self, charactere : Character) -> None:
        """
        Dessine un charactère sur la grille en fonction de son image et de ses coordonnées
        :param charactere: Character à dessiner
        """
        imageCharacter = charactere.recupererImage()
        tailleImageX, tailleImageY = imageCharacter.get_size()
        coordScreenX, coordScreenY = self.convertirCoordNumVersEcran(charactere.getPosition())
        coordScreenX -= tailleImageX / 2
        coordScreenY -= tailleImageY / 2
        self.__screen.blit(imageCharacter, (coordScreenX, coordScreenY))

    def rectBulletEcran(self, bullet : Bullet) -> pygame.Rect:
        """
        :param bullet: Bullet dont on veut la zone à l'écran
        :return: Rectangle occupé par l'image de la bullet à l'écran, centré sur sa position
        """
        rectBullet = pygame.Rect((0, 0), config.tailleBullet)
        rectBullet.center = self.convertirCoordNumVersEcran(bullet.getPosition())
        return rectBullet

    def dessinerBullet(self, bullet : Bullet) -> None:
        """
        Dessine une bullet centrée sur sa position
        :param bullet: Bullet à dessiner
        """
        self.__screen.blit(bullet.recupererImage(), self.rectBulletEcran(bullet))

    def estDansFenetre(self, bullet : Bullet) -> bool:
        """
        :param bullet: Bullet à tester
        :return: True si au moins une partie de la bullet est visible dans la fenêtre
        """
        return self.__screen.get_rect().colliderect(self.rectBulletEcran(bullet))

    def dessinerListeCharacter(self, listCharacter : list[Character]) -> None:
        """
        Dessine une liste de charactère sur la grille
        :param listCharacter: Charactères à dessiner
        """
        for character in listCharacter:
            self.dessinerCharacter(character)

    def dessiner(self, listCharactere=None, vie=None, vieMax=None) -> None:
        """
        Dessine l'ensemble de la fenêtre de jeu
        :param listCharactere: Charactères à dessiner
        """
        self.dessinerGrille()
        if listCharactere:
            self.dessinerListeCharacter(listCharactere)
        if vie is not None and vieMax:
            self.dessinerBarreDeVie(vie, vieMax)

    def dessinerBarreDeVie(self, vie: int, vieMax: int) -> None:
        """Affiche la barre de vie correspondant à la vie restante"""
        if vie <= 0:
            return

        x, y = config.barreViePosition
        largeur, hauteur = self.__imagesBarreVie.get_size()

        marge = 8
        xInt = x + marge
        yInt = y + 10
        largeurInt = largeur - marge
        hauteurInt = hauteur - 20

        pygame.draw.rect(self.__screen, (220, 162, 125), (xInt, yInt, largeurInt, hauteurInt))

        largeurVie = int(largeurInt * vie / vieMax)
        pygame.draw.rect(self.__screen, (0, 200, 0), (xInt, yInt, largeurVie, hauteurInt))

        self.__screen.blit(self.__imagesBarreVie, (x, y))
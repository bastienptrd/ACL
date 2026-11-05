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
                                       config.caseApparitionEnnemi : surf5}

        self.remiseEchelle()

        self.__barreOriginale = pygame.image.load(config.barre_vie_images).convert()
        self.__barreOriginale.set_colorkey((63, 72, 204))
        self.__imagesBarreVie = None
        self.__tailleFenetreBarre = None
        self.__majBarreVie()



    def __majBarreVie(self) -> None:
        """Redimensionne l'image de la barre si la taille de la fenêtre a changé"""
        tailleFenetre = self.__screen.get_size()
        if tailleFenetre == self.__tailleFenetreBarre:
            return  # rien à refaire, on évite de rescaler à chaque frame

        self.__tailleFenetreBarre = tailleFenetre
        largeur = int(tailleFenetre[0] * config.barreVieLargeurRel)
        ratio = self.__barreOriginale.get_height() / self.__barreOriginale.get_width()
        image = pygame.transform.scale(self.__barreOriginale, (largeur, int(largeur * ratio)))
        image.set_colorkey((63, 72, 204))
        self.__imagesBarreVie = image

        self.__longueurRayon = config.longueurMaxRayon
        self.imageLampe = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA)
        self.updateTailleFenetre()

    def dessinerDegat(self):
        # Rempli l'écran de rouge le temps d'une frame
        self.__screen.fill((255, 0, 0))
        pygame.display.flip()

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
        coordScreenX, coordScreenY = self.convertirCoordNumVersEcran(charactere.getPosition())
        tailleX, tailleY = charactere.collisionRect.size
        coordScreenX -= tailleX / 2
        coordScreenY -= tailleY / 2
        rect = pygame.rect.Rect(coordScreenX, coordScreenY, tailleX, tailleY)
        if rect.colliderect(self.__screen.get_rect()):
            imageCharacter = charactere.recupererImage()
            tailleImageX, tailleImageY = imageCharacter.get_size()
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

    def estDansFenetreBullet(self, bullet : Bullet) -> bool:
        """
        :param bullet: Bullet à tester
        :return: True si au moins une partie de la bullet est visible dans la fenêtre
        """
        return self.__screen.get_rect().colliderect(self.rectBulletEcran(bullet))

    def estDansFenetre(self, rect : pygame.rect.Rect) -> bool:
        """
        :param rect: rectangle à tester
        :return: True si au moins une partie de la bullet est visible dans la fenêtre
        """
        return self.__screen.get_rect().colliderect(rect)


    def dessinerListeCharacter(self, listCharacter : list[Character]) -> None:
        """
        Dessine une liste de charactère sur la grille
        :param listCharacter: Charactères à dessiner
        """
        for character in listCharacter:
            if self.estDansFenetre(character.collisionRect):
                self.dessinerCharacter(character)

    def dessinerBarreDeVie(self, vie: int, vieMax: int) -> None:
        """Affiche la barre de vie correspondant à la vie restante"""
        if vie <= 0:
            return

        self.__majBarreVie()

        largeurEcran, hauteurEcran = self.__screen.get_size()
        largeur, hauteur = self.__imagesBarreVie.get_size()

        # Position : en bas à gauche, avec une marge proportionnelle
        x = int(largeurEcran - largeur - largeurEcran * config.barreVieMargeRel[0])
        y = int(hauteurEcran - hauteur - hauteurEcran * config.barreVieMargeRel[1])

        # Marges internes proportionnelles à la taille de la barre
        # (avant : 8 et 10 px pour une barre de 300 px de large)
        marge = int(largeur * 8 / 300)
        decalageY = int(largeur * 10 / 300)

        xInt = x + marge
        yInt = y + decalageY
        largeurInt = largeur - marge
        hauteurInt = hauteur - 2 * decalageY

        pygame.draw.rect(self.__screen, (220, 162, 125), (xInt, yInt, largeurInt, hauteurInt))

        largeurVie = int(largeurInt * vie / vieMax)
        pygame.draw.rect(self.__screen, (0, 200, 0), (xInt, yInt, largeurVie, hauteurInt))

        self.__screen.blit(self.__imagesBarreVie, (x, y))

    def changerLongeurRayon(self, taille: float) -> None:
        self.__longueurRayon = taille
        self.updateTailleFenetre()

    def recupLongeurRayon(self) -> int:
        return self.__longueurRayon

    def updateRayon(self) -> None:
        """
        Refait l'image lampe en fonction de la longueur du rayon
        """
        self.imageLampe.fill((0, 0, 0, 0))
        for i in range(255):
            pygame.draw.circle(self.imageLampe, (0, 0, 0, i), self.__screen.get_rect().center,
                               self.__longueurRayon * config.tailleCaseRendu[0] * (255 - i) / 255)

    def dessinerNoirLampe(self, character : Character, rayons : list[tuple[float, float, float]], opacite) -> None:
        """
        :param character: Point de départ de la lumiere
        :param rayons: Liste des rayons envoyés par le joueur
        :param opacite: Opacité de la lampe
        """
        # Ombre de fond
        ombre = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA)
        ombre.fill((0, 0, 0, config.opaciteFond))

        # Mask pour la lampe
        mask = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 0))

        # Lampe
        lampe = self.imageLampe.copy()

        # On ajoute la forme balayée par la lampe
        pointLampe = [self.convertirCoordNumVersEcran(pygame.Vector2(x, y)) for _,x,y in rayons] + [self.convertirCoordNumVersEcran(character.getPosition())]
        for i in range(0, 20, 2):
            pygame.draw.polygon(mask, (0, 0, 0, opacite * i / 20), pointLampe, config.epaisseurLumiereMur - i)
            for point in pointLampe:
                pygame.draw.circle(mask, (0, 0, 0, opacite * i / 20), point, config.epaisseurLumiereMur / 2 - 1 - i / 2)
        pygame.draw.polygon(mask, (0, 0, 0, opacite), pointLampe)

        # On découpe notre forme dans la lampe
        lampe.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # On ajoute le cercle du joueur à l'ombre
        for i in range(0, config.opaciteCercleLumiereJoueur, 2):
            pygame.draw.circle(ombre, (0, 0, 0, 255 - i), self.convertirCoordNumVersEcran(character.getPosition()),
                                       max(config.rayonLumiereJoueur - i * config.vitesseDegradeCerlceLumiere, 0))

        # On soustrait la lampe à l'ombre
        ombre.blit(lampe, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

        # On dessine finalement l'ombre
        self.__screen.blit(ombre, (0, 0))

    def dessiner(self, listCharactere : list[Character],  dessinerGrille : bool = True, dessinerChararcter : bool = True, dessinerOmbre : bool = True, dessinerBarreVie : bool = True) -> None:
        """
        Dessine l'ensemble de la fenêtre de jeu
        :param dessinerGrille: Dessiner la grille (True par default)
        :param dessinerBarreVie: Dessiner la barre de vie (True par default)
        :param dessinerOmbre: Dessiner les ombres (True par default)
        :param dessinerChararcter: Dessiner les character (True par default)
        :param listCharactere: Charactères à dessiner
        """
        if dessinerGrille:
            self.dessinerGrille()
        if dessinerChararcter:
            self.dessinerListeCharacter(listCharactere)
        if dessinerOmbre:
            # Remplacer le paramètre opacité par la puissance de la lampe (dépend de l'item piles)
            self.dessinerNoirLampe(listCharactere[0], listCharactere[0].envoyerRayonLampe(self.__grille, config.nombreRayon, config.largeurLampe), 245)
        if dessinerBarreVie:
            self.dessinerBarreDeVie(listCharactere[0].health, listCharactere[0].healthMax)

    def updateTailleFenetre(self) -> None:
        """
        Change les dispositions en fonction de lataille de la fenêtre
        """
        self.imageLampe = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA)
        self.updateRayon()
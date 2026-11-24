import math
import time

import pygame

import config
from model.Bullet import Bullet
from model.Character import Character
from model.Entite import Entite
from model.Items import Items


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

        self.__longueurRayon = config.longueurMaxRayon
        self.__imageLampe = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA)
        self.updateTailleFenetre()

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
        """
        Dessine la grille du labyrinthe
        """
        self.__screen.fill((0, 0, 0))

        for i in range(len(self.__grille)):
            for j in range(len(self.__grille[0])):
                self.__screen.blit(self.__imagesCaseLabyrinthe[self.__grille[i][j]], self.convertirCoordNumVersEcran((i, j)))

    #region Entite
    def dessinerEntiter(self, entite : Entite) -> None:
        """
        Dessine un charactère sur la grille en fonction de son image et de ses coordonnées
        :param entite: Character à dessiner
        """
        coordScreenX, coordScreenY = self.convertirCoordNumVersEcran(entite.getPosition())
        tailleX, tailleY = entite.collisionRect.size
        rectCollision = pygame.rect.Rect(0, 0, tailleX, tailleY)
        rectCollision.center = coordScreenX, coordScreenY

        # Si l'objet est dans l'écran
        if rectCollision.colliderect(self.__screen.get_rect()):
            imageCharacter = entite.recupererImage()
            tailleX, tailleY = imageCharacter.get_rect().size
            rectImage = pygame.rect.Rect(0, 0, tailleX, tailleY)
            rectImage.center = coordScreenX, coordScreenY

            if isinstance(entite, Items):
                # On fait la petite animation haut-bas
                rectImage.y += math.sin(time.time() * config.vitesseOcsilation) * config.amplitudeOcsilations

                # On dessine la barre de progression
                progression = entite.progression()
                if progression > 0:
                    hauteurJauge = 6
                    fond = pygame.Rect(rectImage.left, rectImage.top - hauteurJauge - 4, tailleX, hauteurJauge)
                    pygame.draw.rect(self.__screen, (60, 60, 60), fond)
                    remplissage = pygame.Rect(fond.left, fond.top, int(tailleX * progression), hauteurJauge)
                    pygame.draw.rect(self.__screen, (0, 200, 0), remplissage)
                    pygame.draw.rect(self.__screen, (0, 0, 0), fond, width=1)

                tailleX += 20

            if not isinstance(entite, Bullet):
                # On dessine l'ombre sous l'entité
                rectOmbre = pygame.Rect(0, 0, tailleX - 20 + 2 * math.sin(time.time() * config.vitesseOcsilation), config.hauteurOmbreItem)
                surfaceOmbre = pygame.surface.Surface(rectOmbre.size, pygame.SRCALPHA)
                pygame.draw.ellipse(surfaceOmbre, (0, 0, 0, 50), rectOmbre)
                rectOmbre.center = (coordScreenX, coordScreenY + 30)
                self.__screen.blit(surfaceOmbre, (rectOmbre.x, rectOmbre.y))

            # On dessine l'entité
            self.__screen.blit(imageCharacter, (rectImage.x, rectImage.y))

            # Dessin de la boite de collision
            if config.debug:
                surfaceRectCollision = pygame.surface.Surface(entite.collisionRect.size, pygame.SRCALPHA)
                pygame.draw.rect(surfaceRectCollision, (0, 0, 255, 150), (0, 0, surfaceRectCollision.get_width(), surfaceRectCollision.get_height()))
                self.__screen.blit(surfaceRectCollision, (rectCollision.x, rectCollision.y))

    def dessinerListeEntite(self, listEntite : list[Entite]) -> None:
        """
        Dessine une liste de charactère sur la grille
        :param listEntite: Charactères à dessiner
        """
        for entite in listEntite:
            self.dessinerEntiter(entite)

            if config.debug and isinstance(entite, Character) and entite.name != "Player" and entite.name != "Fin":

                # Affichage barre de vie
                progression = entite.health / entite.healthMax
                if progression > 0:
                    largueur = entite.collisionRect.w
                    coordX, coordY = self.convertirCoordNumVersEcran(entite.getPosition())
                    coordX -= entite.collisionRect.w / 2
                    coordY -= entite.collisionRect.h / 2
                    hauteurJauge = 6

                    fond = pygame.Rect(coordX, coordY - hauteurJauge - 4, largueur, hauteurJauge)
                    pygame.draw.rect(self.__screen, (60, 60, 60), fond)

                    remplissage = pygame.Rect(fond.left, fond.top, int(largueur * progression), hauteurJauge)
                    pygame.draw.rect(self.__screen, (0, 200, 0), remplissage)
                    pygame.draw.rect(self.__screen, (0, 0, 0), fond, width=1)

                #affichage du rayon tiré vers le joueur
                _, pointX, pointY = entite.jeterRayon(self.__grille, listEntite[0].getPosition())
                pygame.draw.circle(self.__screen, (255, 255 * int(entite.voit(listEntite[0], self.__grille)), 255),
                                   self.convertirCoordNumVersEcran(pygame.Vector2(pointX, pointY)), 5)
                pygame.draw.line(self.__screen, (100, 100, 100),
                                 self.convertirCoordNumVersEcran(pygame.Vector2(pointX, pointY)),
                                 self.convertirCoordNumVersEcran(entite.getPosition()), 2)
    #endregion

    #region Barre de vie
    def __majBarreVie(self) -> None:
        """
        Redimensionne l'image de la barre si la taille de la fenêtre a changé
        """
        tailleFenetre = self.__screen.get_size()
        if tailleFenetre == self.__tailleFenetreBarre:
            return  # rien à refaire, on évite de rescaler à chaque frame

        self.__tailleFenetreBarre = tailleFenetre
        largeur = int(tailleFenetre[0] * config.barreVieLargeurRel)
        ratio = self.__barreOriginale.get_height() / self.__barreOriginale.get_width()
        image = pygame.transform.scale(self.__barreOriginale, (largeur, int(largeur * ratio)))
        image.set_colorkey((63, 72, 204))
        self.__imagesBarreVie = image

    def dessinerDegat(self):
        # Rempli l'écran de rouge le temps d'une frame
        self.__screen.fill((255, 0, 0))
        pygame.display.flip()

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
    #endregion

    #region Ombre
    def changerLongeurRayon(self, taille: float) -> None:
        self.__longueurRayon = taille
        self.updateTailleFenetre()

    def recupLongeurRayon(self) -> int:
        return self.__longueurRayon

    def updateRayon(self) -> None:
        """
        Refait l'image lampe en fonction de la longueur du rayon
        """
        self.__imageLampe.fill((0, 0, 0, 0))
        for i in range(255):
            pygame.draw.circle(self.__imageLampe, (0, 0, 0, i), self.__screen.get_rect().center,
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
        lampe = self.__imageLampe.copy()

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
        if config.debug:
            # On affiche seulement le contour
            pygame.draw.polygon(self.__screen, (0, 255, 255, 255), pointLampe, 3)
        else :
            self.__screen.blit(ombre, (0, 0))
    #endregion

    def dessiner(self, listCharactere : list[Character],
                 listItem : list[Items],
                 listBullet : list[Bullet],
                 dessinerGrille : bool = True,
                 dessinerEntite : bool = True,
                 dessinerOmbre : bool = True,
                 dessinerBarreVie : bool = True) -> None:
        """
        Dessine l'ensemble de la fenêtre de jeu
        :param dessinerGrille: Dessiner la grille (True par default)
        :param dessinerBarreVie: Dessiner la barre de vie (True par default)
        :param dessinerOmbre: Dessiner les ombres (True par default)
        :param dessinerEntite: Dessiner les entites (True par default)
        :param listCharactere: Charactères à dessiner
        :param listItem: Items à dessiner
        :param listBullet: Bullet à dessiner
        """
        if dessinerGrille:
            self.dessinerGrille()
        if dessinerEntite:
            self.dessinerListeEntite(listCharactere)
            self.dessinerListeEntite(listBullet)
            self.dessinerListeEntite(listItem)
        if dessinerOmbre:
            self.dessinerNoirLampe(listCharactere[0], listCharactere[0].envoyerRayonLampe(self.__grille, config.nombreRayon, config.largeurLampe), listCharactere[0].opacite)
        if dessinerBarreVie:
            self.dessinerBarreDeVie(listCharactere[0].health, listCharactere[0].healthMax)

    def updateTailleFenetre(self) -> None:
        """
        Change les dispositions en fonction de lataille de la fenêtre
        """
        self.__imageLampe = pygame.Surface(self.__screen.get_size(), pygame.SRCALPHA)
        self.updateRayon()
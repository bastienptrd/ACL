import math
import pygame

import config
from model.Entite import Entite

def voisin(x, sens):
    if math.floor(x) == x:
        return int(x + sens)
    return math.floor(x) + int(sens > 0)

class Character (Entite):
    def __init__(self, name : str, health : int , speed : float, position : pygame.Vector2, image_path :str, collisionRect : pygame.rect.Rect, direction : pygame.Vector2) :
        self.health = health
        self.healthMax = health
        self.speed = speed
        self.direction = pygame.Vector2(direction)
        super().__init__(name, position, image_path, collisionRect)


    def subirDegats(self, montant: int) -> None:
        self.health = max(0, self.health - montant)

    def estMort(self) -> bool:
        return self.health <= 0

    def reinitialiserVie(self) -> None:
        self.health = self.healthMax

    def soigner(self, montant: int)->None:
        self.health = min(self.healthMax, self.health+montant)

    def jeterRayon(self, grille : list[list[int]], direction : float | pygame.Vector2) -> tuple[float, float, float]:
        """
        :param grille: Grille du lancer de rayon
        :param direction: Direction en radians du rayon ou vecteur 2d du point visé
        :return: (distance rayon, coordonnées du point de contacte)
        """
        #Départ du rayon
        rayonX, rayonY = self.getPosition()

        if type(direction) == float:
            directionX = math.cos(direction)
            directionY = math.sin(direction)
        else:
            directionX, directionY = (direction - self.getPosition()) / math.sqrt((direction - self.getPosition()) * (direction - self.getPosition()))

        deltaX = abs(1 / directionX) if directionX != 0 else float("inf")
        deltaY = abs(1 / directionY) if directionY != 0 else float("inf")

        pasX = 1 if directionX > 0 else -1
        pasY = 1 if directionY > 0 else -1

        conditions = True

        while conditions:
            distanceCaseX = abs(voisin(rayonX, pasX) - rayonX)
            distanceCaseY = abs(voisin(rayonY, pasY) - rayonY)

            if distanceCaseX * deltaX < distanceCaseY * deltaY:
                rayonX += directionX * distanceCaseX * deltaX
                rayonY += directionY * distanceCaseX * deltaX
            else:
                rayonX += directionX * distanceCaseY * deltaY
                rayonY += directionY * distanceCaseY * deltaY

            caseX = voisin(rayonX, pasX - int(pasX > 0))
            caseY = voisin(rayonY, pasY - int(pasY > 0))

            conditions = 0 <= caseY < len(grille[0]) and 0 <= caseX < len(grille) and grille[caseX][caseY] != config.caseMur and  grille[caseX][caseY] != config.caseObstacle

        distanceParcourue = math.sqrt((rayonX - self.getPosition()[0]) ** 2 + (rayonY - self.getPosition()[1]) ** 2)
        return distanceParcourue, rayonX, rayonY

    def envoyerRayonLampe(self, grille : list[list[int]], nombreRayon : int, fov : float) -> list[tuple[float, float, float]]:
        """
        :param grille: Grille des murs
        :param nombreRayon: Nombre de rayons envoyé
        :param fov: Ecartement des rayons
        :return: liste des poinr de collision avec leurs disances respectives
        """
        # Calcul de la direction du joueur en radian
        x, y = self.direction
        angle = 0
        if x != 0:
            angle = math.atan(y / x) + int(x > 0) * math.pi + math.pi
        elif y > 0:
            angle = math.pi / 2
        elif y < 0:
            angle = - math.pi / 2

        # Envoient des rayons dans toutes les directions du champ de vision
        res = [self.jeterRayon(grille, angle - fov / 2 + i * fov / nombreRayon) for i in range(nombreRayon)]

        return res

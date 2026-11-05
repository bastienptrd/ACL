import pygame
import math
import config

def voisin(x, sens):
    if math.floor(x) == x:
        return int(x + sens)
    return math.floor(x) + int(sens > 0)

class Character :
    def __init__(self, name : str, health : int , speed : float, position : pygame.Vector2, image_path :str, collisionRect : pygame.rect.Rect, direction : pygame.Vector2) :
        self.name = name
        self.health = health
        self.healthMax = health
        self.speed = speed
        self.__position = pygame.Vector2(position)
        self.image_path = image_path
        self.collisionRect = collisionRect
        self.direction = pygame.Vector2(direction)

        # Assure de placer les collionsRest aux bons endroits
        self.setPosition(self.__position)

    def generate_image(self) -> pygame.surface.Surface :
        player_img = pygame.image.load(self.image_path).convert_alpha()
        return player_img

    def subirDegats(self, montant: int) -> None:
        self.health = max(0, self.health - montant)

    def estMort(self) -> bool:
        return self.health <= 0

    def reinitialiserVie(self) -> None:
        self.health = self.healthMax

    def recupererImage(self):
        #Coder les animations ici
        return pygame.transform.scale(self.generate_image(), config.tailleCharacter)

    def setPosition(self, position : pygame.Vector2) -> None:
        """
        Mets à jour les position de tous les éléments de charactère
        :param position: nouvelle position
        """
        self.__position = pygame.Vector2(position)
        self.collisionRect.centerx = int(self.__position.x * config.tailleCaseRendu[0])
        self.collisionRect.centery = int(self.__position.y * config.tailleCaseRendu[1])

    def getPosition(self) -> pygame.Vector2:
        # Renvoie une copie : un Vector2 est modifiable, on évite de changer la position par erreur
        return pygame.Vector2(self.__position)

    def toucheCharacter(self, other : "Character") -> bool:
        """
        :param other: Deuxième character
        :return: Bolléen relatif à la collision de leurs rectangles de collision
        """
        return self.collisionRect.colliderect(other.collisionRect)

    def jeterRayon(self, grille : list[list[int]], direction : float | pygame.Vector2) -> tuple[float, float, float]:
        """
        :param grille: Grille du lancer de rayon
        :param direction: Direction en radians du rayon ou vecteur 2d du point visé
        :return: (distance rayon, coordonnées du point de contacte)
        """
        #Départ du rayon
        rayonX, rayonY = self.__position

        if type(direction) == float:
            directionX = math.cos(direction)
            directionY = math.sin(direction)
        else:
            directionX, directionY = (direction - self.__position) / math.sqrt((direction - self.__position) * (direction - self.__position))

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

        distanceParcourue = math.sqrt((rayonX - self.__position[0]) ** 2 + (rayonY - self.__position[1]) ** 2)
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

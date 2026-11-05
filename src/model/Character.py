import pygame
import config

class Character : 
    def __init__(self, name : str, health : int , speed : float, position : pygame.Vector2, image_path :str, collisionRect : pygame.rect.Rect, direction : pygame.Vector2) :
        self.name = name
        self.health = health
        self.speed = speed
        self.__position = pygame.Vector2(position)
        self.image_path = image_path
        self.collisionRect = collisionRect
        self.direction = pygame.Vector2(direction)

    def generate_image(self) -> pygame.surface.Surface :
        player_img = pygame.image.load(self.image_path).convert_alpha()
        return player_img

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


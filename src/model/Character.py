import pygame
import config

class Character : 
    def __init__(self, name : str, health : int , speed : float, position :tuple[float, float], image_path :str, collisionRect : pygame.rect.Rect):
        self.name = name
        self.health = health
        self.speed = speed
        self.__position = position
        self.image_path = image_path
        self.collisionRect = collisionRect

    def generate_image(self) -> pygame.surface.Surface :
        player_img = pygame.image.load(self.image_path).convert_alpha()
        return player_img

    def recupererImage(self):
        #Coder les animations ici
        return pygame.transform.scale(self.generate_image(), config.tailleCharacter)

    def setPosition(self, position):
        """
        Mets à jour les position de tous les éléments de charactère
        :param position: nouvelle position
        """
        self.collisionRect.centerx = int(position[0] * config.tailleCaseRendu[0])
        self.collisionRect.centery = int(position[1] * config.tailleCaseRendu[1])
        self.__position = position

    def getPosition(self):
        return self.__position


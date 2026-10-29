import pygame
import config

class Character : 
    def __init__(self, name : str, health : int , speed : float, position :tuple[float, float], image_path :str):
        self.name = name
        self.health = health
        self.speed = speed
        self.position = position
        self.image_path = image_path

    def generate_image(self) -> pygame.surface.Surface :
        player_img = pygame.image.load(self.image_path).convert_alpha()
        return player_img

    def recupererImage(self):
        #Coder les animations ici
        return pygame.transform.scale(self.generate_image(), config.tailleCharacter)


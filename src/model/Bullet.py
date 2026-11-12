import pygame
import config
from model.Ennemi import Ennemi


class Bullet:
    # Images déjà chargées, partagées par toutes les bullets (chemin -> image)
    __imagesChargees = {}

    def __init__(self, damage : int, img_path : str, position : pygame.Vector2, direction : pygame.Vector2, speed : float,collisionRect : pygame.rect.Rect) -> None:
        self.damage = damage
        self.img_path = img_path
        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction)
        self.speed = speed
        self.collisionRect = collisionRect

    def generate_image(self) -> pygame.surface.Surface :
        bulette_img = pygame.image.load(self.img_path).convert()
        bulette_img.set_colorkey(pygame.Color('white'))
        return pygame.transform.scale(bulette_img, config.tailleBullet)

    def recupererImage(self) -> pygame.surface.Surface:
        #Coder les animations ici
        # L'image n'est chargée depuis le disque qu'une seule fois, puis réutilisée
        if self.img_path not in Bullet.__imagesChargees:
            Bullet.__imagesChargees[self.img_path] = self.generate_image()
        return Bullet.__imagesChargees[self.img_path]

    def getPosition(self) -> pygame.Vector2:
        return pygame.Vector2(self.position)

    def setPosition(self, position : pygame.Vector2) -> None:
        self.position = pygame.Vector2(position)
        self.collisionRect.centerx = int(self.position.x * config.tailleCaseRendu[0])
        self.collisionRect.centery = int(self.position.y * config.tailleCaseRendu[1])

    def deplacer(self, dt : float) -> None:
        self.setPosition(self.position + self.direction * self.speed * dt)

    def toucheEnnemi(self, other : Ennemi) -> bool:
        return self.collisionRect.colliderect(other.collisionRect)
import pygame

import config
from model.Ennemi import Ennemi
from model.Entite import Entite


class Bullet (Entite):
    def __init__(self, position : pygame.Vector2, direction : pygame.Vector2) -> None:
        super().__init__("Bullet", position, config.bulette_img_path, pygame.rect.Rect(0, 0, config.tailleCollisionBullet[0] * config.tailleCaseRendu[0], config.tailleCollisionBullet[1] * config.tailleCaseRendu[1]))
        self.damage = config.bullet_damage
        self.direction = direction
        self.speed = config.vitesseBullet

    def deplacer(self, dt : float) -> None:
        self.setPosition(self.getPosition() + self.direction * self.speed * dt)

    def toucheEnnemi(self, other : Ennemi) -> bool:
        return self.collisionRect.colliderect(other.collisionRect)
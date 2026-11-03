import pygame
from model.Character import Character


class Player(Character):
    def __init__(self, name : str, health : int, speed : float, position : pygame.Vector2, image_path :str, collisionRect,direction : pygame.Vector2):
        super().__init__(name, health,speed,position = position,image_path=image_path, collisionRect=collisionRect,direction=direction)
        self.healthMax = health

    def subirDegats(self, montant: int) -> None:
        self.health = max(0, self.health - montant)

    def estMort(self) -> bool:
        return self.health <= 0

    def reinitialiserVie(self) -> None:
        self.health = self.healthMax


    def move(self, direction_input,speed, dt):
        if direction_input == "up":
            self.direction = pygame.Vector2(0, -1)
            position_y = self.getPosition()[1] - speed * dt
            self.setPosition(pygame.Vector2(self.getPosition()[0], position_y))
        elif direction_input == "down":
            self.direction = pygame.Vector2(0, 1)
            position_y = self.getPosition()[1] + speed * dt
            self.setPosition(pygame.Vector2(self.getPosition()[0], position_y))
        elif direction_input == "left":
            self.direction = pygame.Vector2(-1, 0)
            position_x = self.getPosition()[0] - speed * dt
            self.setPosition(pygame.Vector2(position_x, self.getPosition()[1]))
        elif direction_input == "right":
            self.direction = pygame.Vector2(1, 0)
            position_x = self.getPosition()[0] + speed * dt
            self.setPosition(pygame.Vector2(position_x, self.getPosition()[1]))

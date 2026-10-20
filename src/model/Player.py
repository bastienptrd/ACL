import config
import pygame

from model.Character import Character


class Player(Character):
    def __init__(self, name, health,speed,position :tuple,image_path :str):
        super().__init__(name, health,speed,position=position,image_path=image_path)


    def move(self, direction_input,speed, dt):
        if direction_input == "up":
            position_y = self.position[1] - speed * dt
            self.position = (self.position[0], position_y)

        elif direction_input == "down":
            position_y = self.position[1] + speed * dt
            self.position = (self.position[0], position_y)
        elif direction_input == "left":
            position_x = self.position[0] - speed * dt
            self.position = (position_x, self.position[1])
        elif direction_input == "right":
            position_x = self.position[0] + speed * dt
            self.position = (position_x, self.position[1])

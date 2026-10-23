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


    def generate_image(self) :
        player_img = pygame.image.load(self.image_path).convert_alpha()
        player_img = pygame.transform.scale(player_img, (player_img.get_width()/15, player_img.get_height()/15))  # Redimensionner l'image du joueur à 50x50 pixels
        return player_img


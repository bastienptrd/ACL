from model.Character import Character


class Player(Character):
    def __init__(self, name : str, health : int, speed : float, position : tuple[float, float], image_path :str, collisionRect):
        super().__init__(name, health,speed,position = position,image_path=image_path, collisionRect=collisionRect)

    def move(self, direction_input,speed, dt):
        if direction_input == "up":
            position_y = self.getPosition()[1] - speed * dt
            self.setPosition((self.getPosition()[0], position_y))
        elif direction_input == "down":
            position_y = self.getPosition()[1] + speed * dt
            self.setPosition((self.getPosition()[0], position_y))
        elif direction_input == "left":
            position_x = self.getPosition()[0] - speed * dt
            self.setPosition((position_x, self.getPosition()[1]))
        elif direction_input == "right":
            position_x = self.getPosition()[0] + speed * dt
            self.setPosition((position_x, self.getPosition()[1]))

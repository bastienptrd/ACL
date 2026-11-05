import pygame
import config
from model.Character import Character


class Player(Character):
    def __init__(self, name : str, health : int, speed : float, position : pygame.Vector2, image_path :str, collisionRect,direction : pygame.Vector2):
        super().__init__(name, health,speed,position = position,image_path=image_path, collisionRect=collisionRect,direction=direction)
        self.healthMax = health
        self.__direction = "down"
        self.__enMouvement = False
        self.__debutAnimation = pygame.time.get_ticks()
        
        def charger_image(chemin):
            image = pygame.image.load(chemin).convert_alpha()

            return pygame.transform.scale(
                image, config.tailleCharacter
            )

        # Animation vers le bas
        bas = [
            charger_image(config.player_bas_path),
            charger_image(config.player_bas_marche1_path),
            charger_image(config.player_bas_marche2_path)
        ]

        # Animation vers la droite
        droite = [
            charger_image(config.player_droite_path),
            charger_image(config.player_droite_marche1_path),
            charger_image(config.player_droite_marche2_path)
        ]

        
        gauche = [
            pygame.transform.flip(image, True, False)
            for image in droite
        ]

       
        self.__animations = {
            "down": bas,
            "right": droite,
            "left": gauche,
            "up": bas  }

    def subirDegats(self, montant: int) -> None:
        self.health = max(0, self.health - montant)

    def estMort(self) -> bool:
        return self.health <= 0

    def reinitialiserVie(self) -> None:
        self.health = self.healthMax


    def move(self, direction_input, speed, dt):

        if direction_input not in self.__animations:
            return

       
        if not self.__enMouvement or direction_input != self.__direction:
            self.__debutAnimation = pygame.time.get_ticks()

        self.__direction = direction_input
        self.__enMouvement = True

        # Déplacement
        x, y = self.getPosition()

        if direction_input == "up":
            self.direction = pygame.Vector2(0, -1)
            y -= speed * dt

        elif direction_input == "down":
            self.direction = pygame.Vector2(0, 1)
            y += speed * dt

        elif direction_input == "left":
            self.direction = pygame.Vector2(-1, 0)

            x -= speed * dt

        elif direction_input == "right":
            self.direction = pygame.Vector2(1, 0)
            x += speed * dt

        self.setPosition((x, y))

    def arreter(self):
        self.__enMouvement = False

    def recupererImage(self):

        images = self.__animations[self.__direction]

        if not self.__enMouvement:
            numeroImage = 0

        else:
            temps = pygame.time.get_ticks() - self.__debutAnimation

            numeroImage = 1 + (temps // 150) % 2

        return images[int(numeroImage)]

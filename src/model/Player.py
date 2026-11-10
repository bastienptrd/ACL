import math

import pygame
import config
from model.Character import Character
from model.Items import Items, TypeItem

class Player(Character):
    def __init__(self, position : pygame.Vector2):
        collisionRectJoueur = pygame.rect.Rect(0, 0, config.tailleCollisionJoueur[0] * config.tailleCaseRendu[0], config.tailleCollisionJoueur[1] * config.tailleCaseRendu[1])
        super().__init__("Player", config.vieJoueur, config.vitesseJoueur, position, config.player_img_path, collisionRectJoueur, pygame.Vector2(0,1))

        self.healthMax = self.health
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

        self.collisionRect = self.recupererImage().get_rect()
        self.setPosition(self.getPosition())

    def move(self, direction_input : str, dt : float) -> None:
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
            y -= self.speed * dt

        elif direction_input == "down":
            self.direction = pygame.Vector2(0, 1)
            y += self.speed * dt

        elif direction_input == "left":
            self.direction = pygame.Vector2(-1, 0)
            x -= self.speed * dt

        elif direction_input == "right":
            self.direction = pygame.Vector2(1, 0)
            x += self.speed * dt

        self.setPosition(pygame.Vector2(x, y))

    def arreter(self):
        self.__enMouvement = False

    def AppliquerItem(self, item :Items)->None:
        if item.typeItem == TypeItem.BANDAGE:
            self.soigner(config.soinBandage)
        elif item.typeItem ==TypeItem.PILE:
            pass #Comportement à voir avec Bastien
        elif item.typeItem == TypeItem.MUNITION :
            pass #Comportement à voir avec Alexis

    def recupererImage(self):
        images = self.__animations[self.__direction]
        if not self.__enMouvement:
            numeroImage = 0
        else:
            temps = pygame.time.get_ticks() - self.__debutAnimation
            numeroImage = 1 + (temps // 150) % 2

        return images[int(numeroImage)]

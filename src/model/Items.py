import pygame
from enum import Enum
import config

class TypeItem(Enum):
    BANDAGE = "bandage"
    PILE = "pile"
    MUNITION = "munition"

class Items:
    __couleurs = {TypeItem.BANDAGE : config.couleurBandage, TypeItem.PILE : config.couleurPile, TypeItem.MUNITION : config.couleurMunition}

    def __init__(self, typeItem : TypeItem, position : pygame.Vector2)->None:
        self.typeItem = typeItem
        self.__position = pygame.Vector2(position)
        self.collisionRect = pygame.rect.Rect(0, 0, config.tailleCollisionItem[0] * config.tailleCaseRendu[0], config.tailleCollisionItem[1] * config.tailleCaseRendu[1])
        self.__tempsSurItem = 0.0
        self.setPosition(self.__position)

    def setPosition(self, position : pygame.Vector2)->None :
        self.__position = pygame.Vector2(position)
        self.collisionRect.centerx = int(self.__position.x * config.tailleCaseRendu[0])
        self.collisionRect.centery = int(self.__position.y * config.tailleCaseRendu[1])

    def getPosition(self)-> pygame.Vector2:
        return pygame.Vector2(self.__position)

    def getCouleur(self) ->tuple[int, int, int]:
        return Items.__couleurs[self.typeItem]

    def toucheCharacter(self, other)->bool:
        return self.collisionRect.colliderect(other.collisionRect)

    def mettreAJour(self, dt :float, joueurSurItem :bool)->bool:
        if joueurSurItem:
            self.__tempsSurItem+=dt
        else :
            self.__tempsSurItem = 0
        return self.__tempsSurItem>=config.tempsRamassageItem

    def progression(self)->float:
        return min(1.0, self.__tempsSurItem/config.tempsRamassageItem)

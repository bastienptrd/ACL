from enum import Enum

import pygame

import config
from model.Entite import Entite


class TypeItem(Enum):
    BANDAGE = "bandage"
    PILE = "pile"
    MUNITION = "munition"

class Items(Entite):
    def __init__(self, typeItem : TypeItem, position : pygame.Vector2)->None:
        self.typeItem = typeItem
        self.__tempsSurItem = 0.0
        super().__init__("Item", position, config.ennemi_imgMort_path, pygame.rect.Rect(0, 0, config.tailleCollisionItem[0] * config.tailleCaseRendu[0], config.tailleCollisionItem[1] * config.tailleCaseRendu[1]))

    def mettreAJour(self, dt :float, joueurSurItem :bool)->bool:
        if joueurSurItem:
            self.__tempsSurItem+=dt
        else :
            self.__tempsSurItem = 0
        return self.__tempsSurItem>=config.tempsRamassageItem

    def progression(self)->float:
        return min(1.0, self.__tempsSurItem/config.tempsRamassageItem)

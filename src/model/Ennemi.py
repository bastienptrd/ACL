import time
from model.Character import *

class Ennemi(Character):
    def __init__(self, name : str, health : int , speed : float, position : pygame.Vector2, image_path :str, collisionRect : pygame.rect.Rect, direction : pygame.Vector2, degatAttaque : int, tempsEntreDeuxAttaque : float, dinstanceVue : float):
        super().__init__(name, health, speed, position, image_path, collisionRect, direction)
        self.degatAttaque = degatAttaque
        self.tempsDerniereAttaque = 0
        self.tempsEntreDeuxAttaque = tempsEntreDeuxAttaque
        self.distanceVue = dinstanceVue

    def voit(self, other : Character, grille : list[list[int]]):
        distance, x, y = self.jeterRayon(grille, other.getPosition())
        distanceOther = math.sqrt((self.getPosition() - other.getPosition()) * (self.getPosition() - other.getPosition()))
        return distance > distanceOther and distanceOther < self.distanceVue

    def peutAttaquer(self):
        return (time.time() - self.tempsDerniereAttaque) > self.tempsEntreDeuxAttaque

    def attaque(self, other : Character) -> bool:
        if self.peutAttaquer():
            other.subirDegats(self.degatAttaque)
            self.tempsDerniereAttaque = time.time()
            return True
        return False

    def move(self, direction : pygame.Vector2):
        self.setPosition(self.getPosition() + direction * config.vitesseEnnemi)

class EnnemiTest(Ennemi):
    def __init__(self, position : pygame.Vector2):
        super().__init__("Ennemi1", config.vieEnnemi, config.vitesseEnnemi, position, config.ennemi_img_path, pygame.rect.Rect(0, 0, config.tailleCollisionEnnemi[0] * config.tailleCaseRendu[0], config.tailleCollisionEnnemi[1] * config.tailleCaseRendu[1]), pygame.Vector2(0, 1), config.degatEnnemi, config.tempsEntreDeuxAttaque, config.distanceVueEnnemi)
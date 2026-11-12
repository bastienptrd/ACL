import time
from model.Character import *

class Ennemi(Character):
    def __init__(self, name : str, health : int , speed : float, position : pygame.Vector2, image_path :str, collisionRect : pygame.rect.Rect, direction : pygame.Vector2, degatAttaque : int, tempsEntreDeuxAttaque : float, dinstanceVue : float):
        super().__init__(name, health, speed, position, image_path, collisionRect, direction)
        self.degatAttaque = degatAttaque
        self.tempsDerniereAttaque = 0
        self.tempsEntreDeuxAttaque = tempsEntreDeuxAttaque
        self.distanceVue = dinstanceVue

    def voit(self, other : Character, grille : list[list[int]]) -> bool:
        """
        :param other: Deuxieme character
        :param grille: Obstacle
        :return: Booléen correspondant à la non-présence d'obstacle entre les deux character
        """
        # On envoie un rayon dans la direction de l'autre character
        distance, x, y = self.jeterRayon(grille, other.getPosition())

        # On calcule la distance entre les deux characters
        distanceOther = math.sqrt((self.getPosition() - other.getPosition()) * (self.getPosition() - other.getPosition()))

        # On renvoie True si le rayon a parcouru plus que la distance qui sépare les deux characters
        return distance > distanceOther and distanceOther < self.distanceVue

    def peutAttaquer(self) -> bool:
        """
        :return: booléen correspondant à la capacité à attaquer
        """
        return (time.time() - self.tempsDerniereAttaque) > self.tempsEntreDeuxAttaque

    def attaque(self, other : Character) -> bool:
        """
        :param other: Character destinataire de l'attaque
        :return: Booléen correspondant a l'execution de l'attaque
        """
        if self.peutAttaquer():
            other.subirDegats(self.degatAttaque)
            self.tempsDerniereAttaque = time.time()
            return True
        return False

    def move(self, direction : pygame.Vector2, dt : float) -> None:
        """
        :param direction: direction du déplacement
        :param dt: temps écoulé depuis la dernière frame
        """
        self.setPosition(self.getPosition() + direction * self.speed * dt)

class EnnemiTest(Ennemi):
    def __init__(self, position : pygame.Vector2):
        super().__init__("Ennemi1", config.vieEnnemi, config.vitesseEnnemi, position, config.ennemi_img_path, pygame.rect.Rect(0, 0, config.tailleCollisionEnnemi[0] * config.tailleCaseRendu[0], config.tailleCollisionEnnemi[1] * config.tailleCaseRendu[1]), pygame.Vector2(0, 1), config.degatEnnemi, config.tempsEntreDeuxAttaque, config.distanceVueEnnemi)
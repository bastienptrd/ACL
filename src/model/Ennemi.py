import time

from model.Character import *


class Ennemi(Character):
    def __init__(self, name: str, health: int, speed: float, position: pygame.Vector2, chemins_images: list[str],
                 imageMort_path: str, collisionRect: pygame.rect.Rect, direction: pygame.Vector2, degatAttaque: int,
                 tempsEntreDeuxAttaque: float, dinstanceVue: float):
        super().__init__(name, health, speed, position, imageMort_path, collisionRect, direction)
        self.imageMort_path = imageMort_path
        self.degatAttaque = degatAttaque
        self.tempsDerniereAttaque = 0
        self.tempsEntreDeuxAttaque = tempsEntreDeuxAttaque
        self.distanceVue = dinstanceVue

        self.images = [
            pygame.image.load(chemin).convert_alpha()
            for chemin in chemins_images
        ]

    def recupererImage(self):
        if self.health <= 0:
            return super().recupererImage()

        numeroImage = (pygame.time.get_ticks() // 200) % len(self.images)

        return pygame.transform.scale(
            self.images[numeroImage],
            config.tailleCharacter
        )

    def voit(self, other: Entite, grille: list[list[int]]) -> bool:
        """
        :param other: Deuxieme character
        :param grille: Obstacle
        :return: Booléen correspondant à la non-présence d'obstacle entre les deux character
        """
        # On envoie un rayon dans la direction de l'autre character
        distance, x, y = self.jeterRayon(grille, other.getPosition())

        # On calcule la distance entre les deux characters
        distanceOther = math.sqrt(
            (self.getPosition() - other.getPosition()) * (self.getPosition() - other.getPosition()))

        # On renvoie True si le rayon a parcouru plus que la distance qui sépare les deux characters
        return distance > distanceOther and distanceOther < self.distanceVue

    def peutAttaquer(self) -> bool:
        """
        :return: booléen correspondant à la capacité à attaquer
        """
        return (time.time() - self.tempsDerniereAttaque) > self.tempsEntreDeuxAttaque

    def attaque(self, other: Character) -> bool:
        """
        :param other: Character destinataire de l'attaque
        :return: Booléen correspondant a l'execution de l'attaque
        """
        if self.peutAttaquer():
            other.subirDegats(self.degatAttaque)
            self.tempsDerniereAttaque = time.time()
            return True
        return False

    def move(self, direction: pygame.Vector2, dt: float) -> None:
        """
        :param direction: direction du déplacement
        :param dt: temps écoulé depuis la dernière frame
        """
        self.setPosition(self.getPosition() + direction * self.speed * dt)


class EnnemiTest(Ennemi):
    def __init__(self, position: pygame.Vector2):
        super().__init__("Ennemi1", config.vieFantome, config.vitesseFantome, position, config.ennemi_img_path,
                         config.ennemi_imgMort_path,
                         pygame.rect.Rect(0, 0, config.tailleCollisionFantome[0] * config.tailleCaseRendu[0],
                                          config.tailleCollisionFantome[1] * config.tailleCaseRendu[1]),
                         pygame.Vector2(0, 1), config.degatFantome, config.tempsEntreDeuxAttaqueFantome,
                         config.distanceVueFantome)


class Fantome(Ennemi):
    def __init__(self, position: pygame.Vector2):
        super().__init__("Fantome",
                         config.vieFantome, config.vitesseFantome, position,
                         [
                             config.fantome_img1_path,
                             config.fantome_img2_path,
                             config.fantome_img3_path
                         ], config.ennemi_imgMort_path,
                         pygame.rect.Rect(0, 0, config.tailleCollisionFantome[0] * config.tailleCaseRendu[0],
                                          config.tailleCollisionFantome[1] * config.tailleCaseRendu[1]),
                         pygame.Vector2(0, 1),
                         config.degatFantome, config.tempsEntreDeuxAttaqueFantome,
                         config.distanceVueFantome)


class MonstreVert(Ennemi):
    def __init__(self, position: pygame.Vector2):
        super().__init__("Monstre vert",
                         config.vieMonstreVert, config.vitesseMonstreVert, position,
                         [
                             config.monstre_vert_img1_path,
                             config.monstre_vert_img2_path,
                             config.monstre_vert_img3_path
                         ], config.ennemi_imgMort_path,
                         pygame.rect.Rect(0, 0, config.tailleCollisionMonstreVert[0] * config.tailleCaseRendu[0],
                                          config.tailleCollisionMonstreVert[1] * config.tailleCaseRendu[1]),
                         pygame.Vector2(0, 1),
                         config.degatMonstreVert, config.tempsEntreDeuxAttaqueMonstreVert,
                         config.distanceVueMonstreVert)

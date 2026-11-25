import pygame, math

import config
from model.Character import Character
from model.Items import Items, TypeItem


class Player(Character):
    def __init__(self, position: pygame.Vector2) -> None:

        collisionRectJoueur = pygame.rect.Rect(0, 0, config.tailleCollisionJoueur[0] * config.tailleCaseRendu[0],
                                               config.tailleCollisionJoueur[1] * config.tailleCaseRendu[1])
        super().__init__("Player", config.vieJoueur, config.vitesseJoueur, position, config.player_img_path,
                         collisionRectJoueur, pygame.Vector2(0, 1))

        self.munition_total = config.nombreMaxBalles
        self.munition_barillet = config.barrilet_capacity

        self.__directionAnimation = "down"
        self.directionVue = pygame.Vector2(0, 1)
        self.__enMouvement = False
        self.__debutAnimation = pygame.time.get_ticks()

        self.opacite = config.opaciteMax
        self.__tempsDepuisReductionOpacite = 0.0

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
            "up": bas}

    def move(self, direction_input: str, dt: float) -> None:
        if direction_input not in self.__animations:
            return

        if not self.__enMouvement or direction_input != self.__directionAnimation:
            self.__debutAnimation = pygame.time.get_ticks()

        self.__directionAnimation = direction_input
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

    def mettreAJourOpacite(self, dt: float) -> None:
        self.__tempsDepuisReductionOpacite += dt
        if self.__tempsDepuisReductionOpacite >= config.tempsReductionOpacite:
            self.opacite = max(0, self.opacite - config.montantReductionOpacite)
            self.__tempsDepuisReductionOpacite = 0.0

    def augmenterOpacite(self) -> None:
        self.opacite = min(config.opaciteMax, self.opacite + config.montantAugmentationOpacite)
        self.__tempsDepuisReductionOpacite = 0.0

    def appliquerItem(self, item: Items) -> None:
        if item.typeItem == TypeItem.BANDAGE:
            self.soigner(config.soinBandage)
        elif item.typeItem == TypeItem.PILE:
            self.augmenterOpacite()
        elif item.typeItem == TypeItem.MUNITION:
            self.munition_total = min(self.munition_total + config.nombreBallesAjouterItem, config.nombreMaxBalles)

    def recupererImage(self):
        images = self.__animations[self.__directionAnimation]
        if not self.__enMouvement:
            numeroImage = 0
        else:
            temps = pygame.time.get_ticks() - self.__debutAnimation
            numeroImage = 1 + (temps // 150) % 2

        return images[int(numeroImage)]

    def recharger(self):
        besoin = config.barrilet_capacity - self.munition_barillet
        if self.munition_total >= besoin:
            self.munition_total -= config.barrilet_capacity - self.munition_barillet
            self.munition_barillet = config.barrilet_capacity
        else:
            self.munition_barillet += self.munition_total
            self.munition_total = 0

    def envoyerRayonLampe(self, grille: list[list[int]], nombreRayon: int, fov: float) -> list[
        tuple[float, float, float]]:
        """
        :param grille: Grille des murs
        :param nombreRayon: Nombre de rayons envoyé
        :param fov: Ecartement des rayons
        :return: liste des poinr de collision avec leurs disances respectives
        """
        # Calcul de la direction du joueur en radian
        x, y = self.directionVue
        angle = 0
        if x != 0:
            angle = math.atan(y / x) + int(x > 0) * math.pi + math.pi
        elif y > 0:
            angle = math.pi / 2
        elif y < 0:
            angle = - math.pi / 2

        # Envoient des rayons dans toutes les directions du champ de vision
        res = [self.jeterRayon(grille, angle - fov / 2 + i * fov / nombreRayon) for i in range(nombreRayon)]

        return res

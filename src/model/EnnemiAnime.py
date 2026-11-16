
import pygame
import config
from model.Ennemi import Ennemi


class EnnemiAnime(Ennemi):

    def __init__(self, position, nom, chemins_images):
        super().__init__(
            nom,
            config.vieEnnemi,
            config.vitesseEnnemi,
            position,
            config.ennemi_img_path,
            config.ennemi_imgMort_path,
            pygame.Rect(
                0, 0,
                config.tailleCollisionEnnemi[0] * config.tailleCaseRendu[0],
                config.tailleCollisionEnnemi[1] * config.tailleCaseRendu[1]
            ),
            pygame.Vector2(0, 1),
            config.degatEnnemi,
            config.tempsEntreDeuxAttaque,
            config.distanceVueEnnemi
        )

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
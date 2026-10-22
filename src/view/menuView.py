import pygame
import config

couleurTexte = (240, 240, 240)
couleurBouton = (94, 38, 38)
couleurBoutonSurvol = (130, 52, 52)
couleurBoutonClic = (130, 52, 52)


class Bouton:
    def __init__(self, texte, centreRelatif, taille, police, image=None, sonClic=None):
        self.__texte = texte
        self.__taille = taille
        self.__centreRelatif = centreRelatif
        self.__rect = pygame.Rect(0, 0, *taille)
        self.__font = pygame.font.SysFont(None, police)
        self.__enfonce = False
        self.__image = None
        self.__sonClic = sonClic

        if image:
            img = pygame.image.load(image).convert_alpha()
            ratio = min(taille[0] / img.get_width(), taille[1] / img.get_height())
            nouvelleTaille = (int(img.get_width() * ratio), int(img.get_height() * ratio))
            self.__image = pygame.transform.smoothscale(img, nouvelleTaille)

    def placer(self, largeur, hauteur):  # Fonction qui recentre le bouton si on bouge la fenetre
        self.__rect.center = (
            int(largeur * self.__centreRelatif[0]),
            int(hauteur * self.__centreRelatif[1]),
        )

    def gererEvenement(self, event):  # Retourne True si on clique...
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
            if self.__rect.collidepoint(event.pos):
                self.__enfonce = True
                if self.__sonClic:
                    self.__sonClic.play()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Relachement du clic
            clique = self.__enfonce and self.__rect.collidepoint(event.pos)
            self.__enfonce = False
            return clique
        return False

    def dessiner(self, surface):
        survol = self.__rect.collidepoint(pygame.mouse.get_pos())  # collidepoint -> check si on est dans le bouton

        if self.__enfonce:
            couleur = couleurBoutonClic
        elif survol:
            couleur = couleurBoutonSurvol
        else:
            couleur = couleurBouton

        if survol:
            rectAff = self.__rect.move(-4, -4)  # Decale de 4px si on survole
        else:
            rectAff = self.__rect

        rayon = 16

        pygame.draw.rect(surface, couleur, rectAff, border_radius=rayon)
        pygame.draw.rect(surface, couleurTexte, rectAff, width=3, border_radius=rayon)

        if self.__image:
            surface.blit(self.__image, self.__image.get_rect(center=rectAff.center))
        else:
            label = self.__font.render(self.__texte, True, couleurTexte)
            surface.blit(label, label.get_rect(center=rectAff.center))


class MenuView:
    def __init__(self, screen, sonClic):
        self.__screen = screen

        self.__fondOriginal = pygame.image.load("C:/Users/user/ACL/assets/images/Bouton/foret_pixel.png").convert()
        self.__fond = pygame.transform.scale(self.__fondOriginal, screen.get_size())

        self.__titreFont = pygame.font.SysFont(None, 110)

        # Boutons du menu principal
        self.__boutonJouer = Bouton("Jouer", (0.5, 0.5), (260, 70), 48, "C:/Users/user/ACL/assets/images/Bouton/JOUER_1.png", sonClic)
        self.__boutonQuitter = Bouton("Quitter", (0.5, 0.65), (260, 70), 48,
                "C:/Users/user/ACL/assets/images/Bouton/QUITTER_1.png", sonClic)
        self.__boutonParametre = Bouton("Paramètres", (0.90, 0.90), (150, 70), 30,
                            "C:/Users/user/ACL/assets/images/Bouton/bouton_parametre.png", sonClic)

        # Boutons des parametres
        self.__boutonAudio = Bouton("Audio", (0.5, 0.5), (260, 75), 48,
                "C:/Users/user/ACL/assets/images/Bouton/AUDIO_1.png", sonClic)
        self.__boutonCommande = Bouton("Commande", (0.5, 0.65), (270,75), 48,
                    "C:/Users/user/ACL/assets/images/Bouton/COMMANDE_1.png", sonClic)
        self.__boutonGameplay = Bouton("Gameplay", (0.5, 0.80), (270, 75), 48,
            "C:/Users/user/ACL/assets/images/Bouton/GAMEPLAY_1.png", sonClic)

        self.__tousLesBoutons = [
            self.__boutonJouer, self.__boutonQuitter, self.__boutonParametre,
            self.__boutonAudio, self.__boutonCommande, self.__boutonGameplay,
        ]

    # Accesseurs
    def getBoutonJouer(self):
        return self.__boutonJouer

    def getBoutonQuitter(self):
        return self.__boutonQuitter

    def getBoutonParametre(self):
        return self.__boutonParametre

    def getBoutonAudio(self):
        return self.__boutonAudio

    def getBoutonCommande(self):
        return self.__boutonCommande

    def getBoutonGameplay(self):
        return self.__boutonGameplay

    def redimensionner(self, largeur, hauteur):
        self.__fond = pygame.transform.scale(self.__fondOriginal, (largeur, hauteur))

    def __placerBoutons(self):
        largeur, hauteur = self.__screen.get_size()
        for b in self.__tousLesBoutons:
            b.placer(largeur, hauteur)

    def __dessinerTitre(self, texte):
        largeur, hauteur = self.__screen.get_size()
        titre = self.__titreFont.render(texte, True, couleurTexte)
        self.__screen.blit(titre, titre.get_rect(center=(largeur // 2, int(hauteur * 0.25))))

    def dessinerMenu(self):
        self.__placerBoutons()
        self.__screen.blit(self.__fond, (0, 0))
        self.__dessinerTitre("JEU PROJET ACL")
        self.__boutonJouer.dessiner(self.__screen)
        self.__boutonQuitter.dessiner(self.__screen)
        self.__boutonParametre.dessiner(self.__screen)

    def dessinerParametres(self):
        self.__placerBoutons()
        self.__screen.blit(self.__fond, (0, 0))
        self.__dessinerTitre("Paramètres du Jeu")
        self.__boutonAudio.dessiner(self.__screen)
        self.__boutonCommande.dessiner(self.__screen)
        self.__boutonGameplay.dessiner(self.__screen)

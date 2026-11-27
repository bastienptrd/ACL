import pygame

import config
from view.menuView import MenuView


def changerVolume(volume, pas):
    # Ajoute "pas" au volume (pas = 0.1 ou -0.1) en restant entre 0 et 1
    volume = round(volume + pas, 1)
    if volume < 0:
        volume = 0
    if volume > 1:
        volume = 1
    return volume


class MenuController:
    def __init__(self, vue : MenuView, sonClic):
        self.__vue = vue
        self.__sonClic = sonClic
        self.__actionEnAttente = None
        self.__difficulteChoisit = 0;

    def getActionEnAttente(self):
        return self.__actionEnAttente

    def gererEvenement(self, event, etat):  # Renvoie dans quel état on se retrouve

        if etat == "menu":
            if self.__vue.getBoutonJouer().gererEvenement(event):
                return "jeu"
            if self.__vue.getBoutonQuitter().gererEvenement(event):
                return "quitter"
            if self.__vue.getBoutonParametre().gererEvenement(event):
                return "parametre"

        elif etat == "parametre":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
            if self.__vue.getBoutonRetour().gererEvenement(event):
                return "menu"
            if self.__vue.getBoutonAudio().gererEvenement(event):
                return "audio"
            if self.__vue.getBoutonCommande().gererEvenement(event):
                return "commande"
            # Pour l'instant ces boutons ne mènent à rien
            if self.__vue.getBoutonGameplay().gererEvenement(event):
                pass

        elif etat == "audio":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "parametre"
            if self.__vue.getBoutonRetour().gererEvenement(event):
                return "parametre"

            # Volume de la musique de fond
            if self.__vue.getBoutonMusiqueMoins().gererEvenement(event):
                config.volumeFond = changerVolume(config.volumeFond, -0.1)
                pygame.mixer.music.set_volume(config.volumeFond)
            if self.__vue.getBoutonMusiquePlus().gererEvenement(event):
                config.volumeFond = changerVolume(config.volumeFond, 0.1)
                pygame.mixer.music.set_volume(config.volumeFond)

            # Volume des bruitages (le clic des boutons)
            if self.__vue.getBoutonSonsMoins().gererEvenement(event):
                config.volumeClic = changerVolume(config.volumeClic, -0.1)
                self.__sonClic.set_volume(config.volumeClic)
            if self.__vue.getBoutonSonsPlus().gererEvenement(event):
                config.volumeClic = changerVolume(config.volumeClic, 0.1)
                self.__sonClic.set_volume(config.volumeClic)

        elif etat == "commande":
            if self.__vue.getBoutonRetour().gererEvenement(event):
                self.__actionEnAttente = None
                return "parametre"
            if self.__actionEnAttente is not None:
                if event.type == pygame.KEYDOWN:
                    if event.key != pygame.K_ESCAPE:
                        config.touches[self.__actionEnAttente] = event.key
                    self.__actionEnAttente = None
                return "commande"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "parametre"
            boutons = self.__vue.getBoutonsCommande()
            for action in boutons:
                if boutons[action].gererEvenement(event):
                    self.__actionEnAttente = action

        elif etat == "fin":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        return etat

    def dessiner(self, etat):
        # Gestion affichage
        if etat == "menu":
            self.__vue.dessinerMenu()
        elif etat == "parametre":
            self.__vue.dessinerParametres()
        elif etat == "audio":
            self.__vue.dessinerAudio()
        elif etat == "commande":
            self.__vue.dessinerCommande(self.getActionEnAttente())
        elif etat == "fin":
            self.__vue.dessinerFin()

    def recupererDifficulte(self) -> int:
        return self.__difficulteChoisit
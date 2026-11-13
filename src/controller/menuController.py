import pygame
import config


def changerVolume(volume, pas):
    # Ajoute "pas" au volume (pas = 0.1 ou -0.1) en restant entre 0 et 1
    volume = round(volume + pas, 1)
    if volume < 0:
        volume = 0
    if volume > 1:
        volume = 1
    return volume


class MenuController:
    def __init__(self, vue, sonClic):
        self.__vue = vue
        self.__sonClic = sonClic

    def gererEvenement(self, event, etat):  # Renvoie dans quel etat on se retrouve

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
            if self.__vue.getBoutonAudio().gererEvenement(event):
                return "audio"
            # Pour l'instant ces boutons ne menent a rien
            if self.__vue.getBoutonCommande().gererEvenement(event):
                pass
            if self.__vue.getBoutonGameplay().gererEvenement(event):
                pass
        elif etat == "audio":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "parametre"
            # Volume de la musique de fond
            if self.__vue.getBoutonMusiqueMoins().gererEvenement(event):
                config.volumeFond = changerVolume(config.volumeFond, -0.1)
                pygame.mixer.music.set_volume(config.volumeFond)
            if self.__vue.getBoutonMusiquePlus().gererEvenement(event):
                config.volumeFond = changerVolume(config.volumeFond, 0.1)
                pygame.mixer.music.set_volume(config.volumeFond)
            # Volume des bruitages
            if self.__vue.getBoutonSonsMoins().gererEvenement(event):
                config.volumeClic = changerVolume(config.volumeClic, -0.1)
                self.__sonClic.set_volume(config.volumeClic)
            if self.__vue.getBoutonSonsPlus().gererEvenement(event):
                config.volumeClic = changerVolume(config.volumeClic, 0.1)
                self.__sonClic.set_volume(config.volumeClic)
        elif etat == "fin":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        return etat

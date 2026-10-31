import pygame


class MenuController:
    def __init__(self, vue):
        self.__vue = vue

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
            # Pour l'instant ces boutons ne menent a rien
            if self.__vue.getBoutonAudio().gererEvenement(event):
                pass
            if self.__vue.getBoutonCommande().gererEvenement(event):
                pass
            if self.__vue.getBoutonGameplay().gererEvenement(event):
                pass

        elif etat == "fin":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        return etat

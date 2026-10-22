import sys
import pygame

from view.menuView import MenuView
from view.gameView import GameView
from controller.menuController import MenuController


class GameController:
    def __init__(self, vue):
        self.__vue = vue

    def gererEvenement(self, event, etat):  # Renvoie dans quel etat on se trouve (menu, jeu, parametre...)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "menu"
        return etat


    def lancerJeu():

        pygame.init()

        # Grille labyrinthe

        grille = [[0 for _ in range(20)] for _ in range(15)]
        for j in range(20):
            grille[0][j] = 1
            grille[14][j] = 1
        for i in range(15):
            grille[i][0] = 1
            grille[i][19] = 1

        murs = [
            (1, 4), (1, 11),
            (2, 2), (2, 4), (2, 6), (2, 7), (2, 8), (2, 9), (2, 11), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17),
            (3, 2), (3, 6), (3, 11),
            (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 8), (4, 9), (4, 10), (4, 11), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17),
            (5, 8), (5, 13),
            (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 8), (6, 10), (6, 11), (6, 13), (6, 15), (6, 16), (6, 17),
            (7, 1), (7, 2), (7, 6), (7, 8), (7, 11), (7, 15),
            (8, 2), (8, 4), (8, 6), (8, 8), (8, 9), (8, 10), (8, 11), (8, 13), (8, 14), (8, 15), (8, 16), (8, 18),
            (9, 4), (9, 12),
            (10, 2), (10, 3), (10, 4), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (10, 11), (10, 12), (10, 14), (10, 15), (10, 16), (10, 17),
            (11, 6), (11, 14),
            (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (12, 14), (12, 15), (12, 16), (12, 17),
        ]
        for i, j in murs:
            grille[i][j] = 1

        # Initialisation de la musique et des sons
        pygame.mixer.init()

        pygame.mixer.music.load("C:/Users/user/ACL/assets/sounds/Bruit_foret.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        sonClic = pygame.mixer.Sound("C:/Users/user/ACL/assets/sounds/clic_2.wav")
        sonClic.set_volume(1)

        # Initialisation de la fenetre
        screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
        pygame.display.set_caption("Interface Provisoire")
        clock = pygame.time.Clock()

        # Appels des classes dans les autres fichiers
        menuView = MenuView(screen, sonClic)
        gameView = GameView(screen, menuView, grille)
        menuController = MenuController(menuView)
        gameController = GameController(gameView)

        # Boucle principale
        etat = "menu"
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    menuView.redimensionner(event.w, event.h)

                if etat in ("menu", "parametre"):
                    etat = menuController.gererEvenement(event, etat)
                elif etat == "jeu":
                    etat = gameController.gererEvenement(event, etat)

                if etat == "quitter":
                    running = False

            if etat == "menu":
                menuView.dessinerMenu()
            elif etat == "parametre":
                menuView.dessinerParametres()
            elif etat == "jeu":
                gameView.dessiner()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

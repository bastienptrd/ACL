import sys
import pygame

import config
from model.maze import Maze
from model.Player import Player
from view.menuView import MenuView
from view.gameView import GameView
from controller.menuController import MenuController


class GameController:
    def __init__(self, vue):
        self.__vue = vue

    @staticmethod
    def gererEvenement(event, etat):  # Renvoie dans quel etat on se trouve (menu, jeu, parametre...)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "menu"
        return etat

    @staticmethod
    def player_mouvement(dt, player):
        if pygame.key.get_pressed()[pygame.K_UP]:
            player.move("up", player.speed, dt)
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            player.move("down", player.speed, dt)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            player.move("left", player.speed, dt)
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            player.move("right", player.speed, dt)

    @staticmethod
    def lancerJeu():

        pygame.init()

        # Initialisation de la musique et des sons
        pygame.mixer.init()

        pygame.mixer.music.load(config.musique_foret_path)
        pygame.mixer.music.set_volume(config.volumeFond)
        pygame.mixer.music.play(-1)

        sonClic = pygame.mixer.Sound(config.son_clic_path)
        sonClic.set_volume(config.volumeClic)

        # Initialisation de la fenêtre
        screen = pygame.display.set_mode(config.screenSize, pygame.RESIZABLE)
        pygame.display.set_caption("Interface Provisoire")
        clock = pygame.time.Clock()

        # initialisation du Labyrinthe
        labyrinthe = Maze()
        labyrinthe.creerLabyrinthe()
        labyrinthe.remplacerMurObstacles(config.nombreObstacle)
        labyrinthe.ajouterApparitionEnemi(config.nombreApparitionEnemi)

        #initialisation du Player
        debutLabyrinthe = labyrinthe.recupDebut()
        positionInitiale = (debutLabyrinthe[0] + 0.5, debutLabyrinthe[1] + 0.5)
        player = Player("Player", config.vieJoueur, config.vitesseJoueur, positionInitiale, config.player_img_path)



        # Appels des classes dans les autres fichiers
        menuView = MenuView(screen, sonClic)
        gameView = GameView(screen, labyrinthe.grille, tailleRenduCase=config.tailleCaseRendu)
        menuController = MenuController(menuView)
        gameController = GameController(gameView)

        # Boucle principale
        etat = "menu"
        running = True

        while running:

            dt = clock.tick(config.imageParSeconde) / 1000.0  # Temps écoulé depuis la dernière frame en secondes

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
                # Si possible à déplacer dans gererEvenement()
                gameController.player_mouvement(dt, player)

                # Place la caméra sur le joueur
                gameView.changePosition(player.position)
                # Dessine le plateau de jeu avec les character
                gameView.dessiner([player])

            pygame.display.flip()

        pygame.quit()
        sys.exit()





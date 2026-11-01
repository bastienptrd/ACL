import sys
import pygame

import config
from model.Character import Character
from model.maze import Maze
from model.Player import Player
from model.Collision import Collisions
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
    def player_mouvement(dt, player, collision):
        for key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            anciennePosition = player.getPosition()
            if pygame.key.get_pressed()[key]:
                player.move(pygame.key.name(key), player.speed, dt)
                if collision.touche_un_mur(player.collisionRect):
                    player.setPosition(anciennePosition)

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
        finLabytinthe = labyrinthe.recupFin()
        positionInitiale = (debutLabyrinthe[0] + 0.5, debutLabyrinthe[1] + 0.5)
        positionFin = (finLabytinthe[0] + 0.5, finLabytinthe[1] + 0.5)

        # Attention les rectangle doivent être de la taille de rendu pour fonctionner dans collision cf Ethan
        collisionRectJoueur = pygame.rect.Rect(0, 0, config.tailleCollisionJoueur[0] * config.tailleCaseRendu[0], config.tailleCollisionJoueur[1] * config.tailleCaseRendu[1])
        collisionRectJoueur.centerx = positionInitiale[0] * config.tailleCaseRendu[0]
        collisionRectJoueur.centery = positionInitiale[1] * config.tailleCaseRendu[1]
        collisionRectFin = pygame.rect.Rect(0, 0, config.tailleCollisionFin[0] * config.tailleCaseRendu[0], config.tailleCollisionFin[1] * config.tailleCaseRendu[1])
        collisionRectFin.centerx = positionFin[0] * config.tailleCaseRendu[0]
        collisionRectFin.centery = positionFin[1] * config.tailleCaseRendu[1]

        player = Player("Player", config.vieJoueur, config.vitesseJoueur, positionInitiale, config.player_img_path, collisionRectJoueur)
        fin = Character("Fin", 0, 0, positionFin, config.player_img_path, collisionRectFin)

        collision = Collisions()
        collision.murs_depuis_grille(labyrinthe.grille, config.tailleCaseRendu)

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

            # Gestion des event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    menuView.redimensionner(event.w, event.h)

                if etat in ("menu", "parametre", "fin"):
                    etat = menuController.gererEvenement(event, etat)
                elif etat == "jeu":
                    etat = gameController.gererEvenement(event, etat)
                if etat == "quitter":
                    running = False

            if etat == "jeu":
                gameController.player_mouvement(dt, player, collision)
                if player.collisionRect.colliderect(fin.collisionRect):
                    etat = "fin"


            # Gestion affichage
            if etat == "menu":
                menuView.dessinerMenu()
            elif etat == "parametre":
                menuView.dessinerParametres()
            elif etat == "jeu":
                # Place la caméra sur le joueur
                gameView.changePosition(player.getPosition())
                # Dessine le plateau de jeu avec les character
                gameView.dessiner([player, fin])
            elif etat == "fin":
                menuView.dessinerFin()

            pygame.display.flip()

        pygame.quit()
        sys.exit()





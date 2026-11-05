import sys
import pygame
import math

import config
from model.Character import Character
from model.Bullet import Bullet
from model.Ennemi import Ennemi
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
    def gererEvenement(event, etat, player):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            if event.key == config.toucheTestDegats:
                pygame.event.post(pygame.event.Event(config.EVENT_DEGATS, montant=config.degatsTest))
        elif event.type == config.EVENT_DEGATS:
            player.subirDegats(event.montant)
            if player.estMort():
                return "fin"
        return etat

    @staticmethod
    def player_mouvement(dt, player, collision):

        deplacement = False

        for key in [pygame.K_UP, pygame.K_DOWN,
                pygame.K_LEFT, pygame.K_RIGHT]:

            anciennePosition = player.getPosition()

            if pygame.key.get_pressed()[key]:

                deplacement = True

                player.move(
                pygame.key.name(key),
                player.speed,
                dt
            )

                if collision.touche_un_mur(player.collisionRect):
                    player.setPosition(anciennePosition)
                    player.arreter()

    # Si aucune touche n'est pressée, le personnage s'arrête
        if not deplacement:
            player.arreter()



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
        labyrinthe.ajouterApparitionEnnemi(config.nombreApparitionEnemi)

        #initialisation du Player
        debutLabyrinthe = labyrinthe.recupDebut()
        finLabytinthe = labyrinthe.recupFin()
        # + 0.5 pour placer le personnage au centre de la case
        positionInitiale = pygame.Vector2(debutLabyrinthe) + pygame.Vector2(0.5, 0.5)
        positionFin = pygame.Vector2(finLabytinthe) + pygame.Vector2(0.5, 0.5)

        # Attention les rectangle doivent être de la taille de rendu pour fonctionner dans collision cf Ethan
        collisionRectJoueur = pygame.rect.Rect(0, 0, config.tailleCollisionJoueur[0] * config.tailleCaseRendu[0], config.tailleCollisionJoueur[1] * config.tailleCaseRendu[1])
        collisionRectJoueur.centerx = positionInitiale.x * config.tailleCaseRendu[0]
        collisionRectJoueur.centery = positionInitiale.y * config.tailleCaseRendu[1]
        collisionRectFin = pygame.rect.Rect(0, 0, config.tailleCollisionFin[0] * config.tailleCaseRendu[0], config.tailleCollisionFin[1] * config.tailleCaseRendu[1])
        collisionRectFin.centerx = positionFin.x * config.tailleCaseRendu[0]
        collisionRectFin.centery = positionFin.y * config.tailleCaseRendu[1]

        player = Player("Player", config.vieJoueur, config.vitesseJoueur, positionInitiale, config.player_img_path, collisionRectJoueur, pygame.Vector2(0,1))
        fin = Character("Fin", 0, 0, positionFin, config.player_bas_path, collisionRectFin, pygame.Vector2(0,1))

        listEnnemi = []
        for (x, y) in labyrinthe.recupCasesApparitionEnnemi():
            x += 0.5
            y += 0.5
            collisionRectEnnemi = pygame.rect.Rect(0, 0, config.tailleCollisionEnnemi[0] * config.tailleCaseRendu[0], config.tailleCollisionEnnemi[1] * config.tailleCaseRendu[1])
            collisionRectEnnemi.centerx = x * config.tailleCaseRendu[0]
            collisionRectEnnemi.centery = y * config.tailleCaseRendu[1]
            listEnnemi.append(Ennemi("Enemi", config.vieEnnemi, config.vitesseEnnemi, pygame.Vector2(x, y), config.ennemi_img_path, collisionRectEnnemi, pygame.Vector2(0,1)))

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
        bullet_list = []
        while running:

            dt = clock.tick(config.imageParSeconde) / 1000.0  # Temps écoulé depuis la dernière frame en secondes
            # Gestion des event
            for event in pygame.event.get():
                # Projectile
                if etat == "jeu" and event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    bullet = Bullet(10, config.bulette_img_path, player.getPosition(), player.direction, speed=config.vitesseBullet)
                    bullet_list.append(bullet)
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    menuView.redimensionner(event.w, event.h)

                if etat in ("menu", "parametre", "fin"):
                    etat = menuController.gererEvenement(event, etat)
                elif etat == "jeu":
                    etat = gameController.gererEvenement(event, etat, player)
                if etat == "quitter":
                    running = False

            if etat == "jeu":
                gameController.player_mouvement(dt, player, collision)
                if player.collisionRect.colliderect(fin.collisionRect):
                    etat = "fin"
                for ennemi in listEnnemi:
                    if ennemi.toucheCharacter(player):
                        pygame.event.post(pygame.event.Event(config.EVENT_DEGATS, montant=config.degatEnnemi))
                        player.setPosition(player.getPosition() - (ennemi.getPosition() - player.getPosition()) * config.reculEnnemi)


            # Gestion affichage
            if etat == "menu":
                menuView.dessinerMenu()
            elif etat == "parametre":
                menuView.dessinerParametres()
            elif etat == "jeu":
                # Place la caméra sur le joueur
                gameView.changePosition(player.getPosition())
                # Dessine le plateau de jeu avec les character
                gameView.dessiner([player, fin] + listEnnemi, player.health, player.healthMax)
                for bullet in bullet_list:
                    bullet.deplacer(dt)
                    gameView.dessinerBullet(bullet)
                # Supprime les bullets sorties de la fenêtre
                bullet_list = [bullet for bullet in bullet_list if gameView.estDansFenetre(bullet)]
            elif etat == "fin":
                menuView.dessinerFin()

            pygame.display.flip()

        pygame.quit()
        sys.exit()





import sys
import pygame
import math

import config
from model.Character import Character
from model.Bullet import Bullet
from model.Ennemi import EnnemiTest, Ennemi
from model.maze import Maze
from model.Player import Player
from model.Collision import Collisions
from view.menuView import MenuView
from view.gameView import GameView
from controller.menuController import MenuController
from model.Items import Items, TypeItem



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
            if player.estMort():
                return "fin"
        return etat

    @staticmethod
    def player_mouvement(dt, player, collision):
        deplacement = False
        for key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            anciennePosition = player.getPosition()

            if pygame.key.get_pressed()[key]:
                deplacement = True

                player.move(pygame.key.name(key), dt)
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
        collisionRectFin = pygame.rect.Rect(0, 0, config.tailleCollisionFin[0] * config.tailleCaseRendu[0], config.tailleCollisionFin[1] * config.tailleCaseRendu[1])

        player = Player(positionInitiale,30,munition_barillet=6)
        fin = Character("Fin", 0, 0, positionFin, config.player_bas_path, collisionRectFin, pygame.Vector2(0,1))

        listEnnemi : list[Ennemi] = []
        for (x, y) in labyrinthe.recupCasesApparitionEnnemi():
            x += 0.5
            y += 0.5
            listEnnemi.append(EnnemiTest(pygame.Vector2(x, y)))


        #Création des items
        typesItems = ([TypeItem.BANDAGE]*config.nombreBandage +[TypeItem.PILE]*config.nombrePile + [TypeItem.MUNITION]*config.nombreMunition)

        casesItems = labyrinthe.choisirCaseItems(len(typesItems))

        listItems = []
        for typeItem, (x, y) in zip(typesItems, casesItems):
            listItems.append(Items(typeItem, pygame.Vector2(x + 0.5, y + 0.5)))

        listCharacter = [player, fin] + listEnnemi

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
        reaload_input_press_time = 0
        temps_de_recharge = 0
        relaod_button_pressed = False
        while running:
            dt = clock.tick(config.imageParSeconde) / 1000.0  # Temps écoulé depuis la dernière frame en secondes
            if abs(reaload_input_press_time - pygame.time.get_ticks()) > temps_de_recharge and relaod_button_pressed:
                player.recharger()
                print(player.munition_barillet)
                relaod_button_pressed = False
            # Gestion des event
            for event in pygame.event.get():
                # Projectile
                if etat == "jeu" and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    reaload_input_press_time = pygame.time.get_ticks()
                    temps_de_recharge = config.temps_de_recharge
                    relaod_button_pressed = True


                if etat == "jeu" and event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    if player.munition_barillet != 0 :
                        player.munition_barillet -= 1
                        print(f"nombre de munitions dans le barrilet :{player.munition_barillet} ")
                        print(f"nombre de munitions de stockage :{player.munition_total} ")
                        taille_rect_bullet = pygame.rect.Rect(0, 0, config.tailleCollisionBullet[0] * config.tailleCaseRendu[0], config.tailleCollisionBullet[1] * config.tailleCaseRendu[1])
                        bullet = Bullet(10, config.bulette_img_path, player.getPosition(), player.direction, speed=config.vitesseBullet, collisionRect=taille_rect_bullet)
                        bullet_list.append(bullet)
                    else :
                        print("plus de munitions ! Recharger")
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    menuView.redimensionner(event.w, event.h)
                    gameView.updateTailleFenetre()

                if etat in ("menu", "parametre", "fin"):
                    etat = menuController.gererEvenement(event, etat)
                elif etat == "jeu":
                    etat = gameController.gererEvenement(event, etat, player)
                if etat == "quitter":
                    running = False

            if etat == "jeu":
                gameController.player_mouvement(dt, player, collision)
                player.mettreAJourOpacite(dt)
                if player.toucheCharacter(fin):
                    etat = "fin"
                for ennemi in listEnnemi:
                    if ennemi.toucheCharacter(player):
                        # Attaque de l'ennemi
                        if ennemi.attaque(player):
                            gameView.dessinerDegat()
                        gameView.changerLongeurRayon(player.health / player.healthMax * (config.longueurMaxRayon - config.longueurMinRayon) + config.longueurMinRayon)
                        pygame.event.post(pygame.event.Event(config.EVENT_DEGATS))

                    elif ennemi.voit(player, labyrinthe.grille):
                        # Déplacement de l'ennemi
                        anciennePosition = ennemi.getPosition()
                        direction = player.getPosition() - ennemi.getPosition()
                        direction = direction / math.sqrt(direction * direction)

                        ennemi.move(pygame.Vector2(direction[0], 0), dt)
                        if collision.touche_un_mur(ennemi.collisionRect):
                            ennemi.setPosition(anciennePosition)
                        ennemi.move(pygame.Vector2(0, direction[1]), dt)
                        if collision.touche_un_mur(ennemi.collisionRect):
                            ennemi.setPosition(anciennePosition)
                    for bullet in bullet_list[:]:
                        if bullet.toucheEnnemi(ennemi) :
                            ennemi.subirDegats(config.bullet_damage)
                            bullet_list.remove(bullet)
                            print(ennemi.health)
                for item in listItems[:]:
                    if item.mettreAJour(dt, item.toucheCharacter(player)):
                        player.AppliquerItem(item)
                        listItems.remove(item)


            # Gestion affichage
            if etat == "menu":
                menuView.dessinerMenu()
            elif etat == "parametre":
                menuView.dessinerParametres()
            elif etat == "jeu":
                # Place la caméra sur le joueur
                gameView.changePosition(player.getPosition())
                # Dessine le plateau de jeu avec les character
                gameView.dessiner(listCharacter, listItems)
                for bullet in bullet_list[:]:
                    bullet.deplacer(dt)
                    gameView.dessinerBullet(bullet)
                    if collision.bullet_touche_mur(bullet.collisionRect) :
                        bullet_list.remove(bullet)
                # Supprime les bullets sorties de la fenêtre
                #bullet_list = [bullet for bullet in bullet_list if gameView.estDansFenetreBullet(bullet)]
            elif etat == "fin":
                menuView.dessinerFin()

            pygame.display.flip()

        pygame.quit()
        sys.exit()





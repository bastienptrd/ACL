import config
import sons
from model.Bullet import Bullet
from model.Collision import Collisions
from model.Ennemi import *
from model.Items import Items, TypeItem
from model.Player import Player
from model.maze import Maze
from view.gameView import GameView


class GameController:
    def __init__(self, vue : GameView):
        self.__vue = vue
        self.__labyrinthe = None
        self.__collision = None

        self.__player = None
        self.__fin = None

        self.__listEnnemi = []
        self.__listItems = []

        self.__bulletList = []
        self.__reaload_input_press_time = 0
        self.__temps_de_recharge = 0
        self.__relaod_button_pressed = False

    def initialiserVariable(self, difficulte : int = 0) -> None:
        """
        :param difficulte: Entier représentant la difficulté
        """
        # initialisation du Labyrinthe
        tailleLabyrintheX, tailleLabyrintheY = config.tailleLabyrintheDifficulte[difficulte]
        self.__labyrinthe = Maze(tailleLabyrintheX, tailleLabyrintheY)
        self.__labyrinthe.creerLabyrinthe()
        self.__labyrinthe.remplacerMurObstacles(config.nombreObstacle)
        self.__labyrinthe.ajouterApparitionEnnemi(config.nombreApparitionEnemiDifficulte[difficulte])

        # initialisation du Player
        debutLabyrinthe = self.__labyrinthe.recupDebut()
        finLabytinthe = self.__labyrinthe.recupFin()
        # + 0.5 pour placer le personnage au centre de la case
        positionInitiale = pygame.Vector2(debutLabyrinthe) + pygame.Vector2(0.5, 0.5)
        positionFin = pygame.Vector2(finLabytinthe) + pygame.Vector2(0.5, 0.5)

        # Attention les rectangle doivent être de la taille de rendu pour fonctionner dans Collision voir avec Ethan
        collisionRectFin = pygame.rect.Rect(0, 0, config.tailleCollisionFin[0] * config.tailleCaseRendu[0], config.tailleCollisionFin[1] * config.tailleCaseRendu[1])

        self.__player = Player(positionInitiale)
        self.__fin = Entite("Fin", positionFin, config.player_bas_path, collisionRectFin)

        self.__listEnnemi: list[Ennemi] = []

        for i, (x, y) in enumerate(self.__labyrinthe.recupCasesApparitionEnnemi()):
            x += 0.5
            y += 0.5
            position = pygame.Vector2(x, y)
            if i % 2 == 0:
                ennemi = Fantome(position)
            else:
                ennemi = MonstreVert(position)
            self.__listEnnemi.append(ennemi)

        # Création des items
        typesItems = ([TypeItem.BANDAGE] * config.nombreBandageDifficulte[difficulte] + [TypeItem.PILE] * config.nombrePileDifficulte[difficulte] + [TypeItem.MUNITION] * config.nombreMunitionDifficulte[difficulte])

        casesItems = self.__labyrinthe.choisirCaseItems(len(typesItems))

        self.__listItems = []
        for typeItem, (x, y) in zip(typesItems, casesItems):
            self.__listItems.append(Items(typeItem, pygame.Vector2(x + 0.5, y + 0.5)))

        self.__collision = Collisions()
        self.__collision.murs_depuis_grille(self.__labyrinthe.grille, config.tailleCaseRendu)
        self.__bulletList = []

        self.__vue.changeGrille(self.__labyrinthe.grille)
        pygame.mixer.stop()  # nouvelle partie : on coupe les sons de la précédente

    def __player_mouvement(self, dt):
        deplacement = False
        mouvements = [("Haut", "up"), ("Bas", "down"), ("Gauche", "left"), ("Droite", "right")]
        for action, direction in mouvements:
            key = config.touches[action]
            anciennePosition = self.__player.getPosition()

            if pygame.key.get_pressed()[key]:
                deplacement = True

                self.__player.move(direction, dt)
                if self.__collision.touche_un_mur(self.__player.collisionRect):
                    self.__player.setPosition(anciennePosition)
                    self.__player.arreter()

        # Si aucune touche n'est pressée, le personnage s'arrête
        if not deplacement:
            self.__player.arreter()
        else:
            sons.repeter("pas")

    def gererEvenement(self, event):
        # Projectile
        if event.type == pygame.KEYDOWN:
            if event.key == config.touches["Recharger"]:
                self.__reaload_input_press_time = pygame.time.get_ticks()
                self.__temps_de_recharge = config.temps_de_recharge
                self.__relaod_button_pressed = True
                sons.jouer("recharge" if self.__player.munition_total > 0 else "vide")

            if event.key == config.touches["Tirer"]:
                if self.__player.munition_barillet != 0:
                    self.__player.munition_barillet -= 1
                    print(f"nombre de munitions dans le barrilet :{self.__player.munition_barillet} ")
                    print(f"nombre de munitions de stockage :{self.__player.munition_total} ")
                    bullet = Bullet(self.__player.getPosition(), self.__player.direction)
                    self.__bulletList.append(bullet)
                    sons.jouer("tir")
                    if self.__player.munition_barillet == 0:
                        sons.jouer("dernier_tir")
                else:
                    print("plus de munitions ! Recharger")
                    sons.jouer("vide")

            if event.key == pygame.K_ESCAPE:
                return "menu"
            if event.key == config.combinaisonToucheDebug[config.toucheValiderDebug]:
                if config.toucheValiderDebug + 1 == len(config.combinaisonToucheDebug):
                    config.debug = not config.debug
                else:
                    config.toucheValiderDebug += 1
            else:
                config.toucheValiderDebug = 0
        elif event.type == pygame.KEYUP:
            config.toucheValiderDebug = 0

        elif event.type == pygame.VIDEORESIZE:
            self.__vue.updateTailleFenetre()

        elif event.type == config.EVENT_DEGATS:
            if self.__player.estMort():
                sons.jouer("mort")
                return "fin"

        if self.__player.toucheEntite(self.__fin):
            sons.jouer("victoire")
            return "fin"

        return "jeu"

    def updateJeu(self, dt):
        if abs(self.__reaload_input_press_time - pygame.time.get_ticks()) > self.__temps_de_recharge and self.__relaod_button_pressed:
            self.__player.recharger()
            print(self.__player.munition_barillet)
            self.__relaod_button_pressed = False

        self.__player_mouvement(dt)
        self.__player.mettreAJourOpacite(dt)
        sons.jouerSonsJeu(self.__player, self.__listEnnemi, self.__fin)

        for ennemi in self.__listEnnemi:
            if ennemi.health <= 0:
                continue
            if ennemi.toucheEntite(self.__player):
                # Attaque de l'ennemi
                if ennemi.attaque(self.__player):
                    pygame.event.post(pygame.event.Event(config.EVENT_DEGATS))
                    self.__vue.dessinerDegat()
                    sons.jouer("degat", 1, sons.cote(self.__player, ennemi))
                    self.__vue.changerLongueurRayonViePlayer(self.__player)

            elif ennemi.voit(self.__player, self.__labyrinthe.grille):
                # Déplacement de l'ennemi
                sons.repeter("poursuite", 1, sons.cote(self.__player, ennemi))
                anciennePosition = ennemi.getPosition()
                direction = self.__player.getPosition() - ennemi.getPosition()
                direction = direction / math.sqrt(direction * direction)

                ennemi.move(pygame.Vector2(direction[0], 0), dt)
                if self.__collision.touche_un_mur(ennemi.collisionRect):
                    ennemi.setPosition(anciennePosition)
                ennemi.move(pygame.Vector2(0, direction[1]), dt)
                if self.__collision.touche_un_mur(ennemi.collisionRect):
                    ennemi.setPosition(anciennePosition)

            for bullet in self.__bulletList[:]:
                if bullet.toucheEnnemi(ennemi):
                    ennemi.subirDegats(config.bullet_damage)
                    sons.jouer("monstre_mort" if ennemi.estMort() else "monstre_touche", 1, sons.cote(self.__player, ennemi))
                    self.__bulletList.remove(bullet)

        for item in self.__listItems[:]:
            if item.mettreAJour(dt, item.toucheEntite(self.__player)):
                sons.jouer(item.typeItem.value)
                self.__player.appliquerItem(item)
                self.__listItems.remove(item)
                self.__vue.changerLongueurRayonViePlayer(self.__player)
            elif item.progression() > 0:
                sons.repeter("ramassage")

        for bullet in self.__bulletList[:]:
            bullet.deplacer(dt)
            if self.__collision.bullet_touche_mur(bullet.collisionRect):
                sons.jouer("impact")
                self.__bulletList.remove(bullet)

    def dessiner(self) -> None:
        # Place la caméra sur le joueur
        self.__vue.changePosition(self.__player.getPosition())
        # Dessine le plateau de jeu avec les character
        self.__vue.dessiner([self.__player, self.__fin] + self.__listItems + self.__bulletList + self.__listEnnemi)
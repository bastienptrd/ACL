import pygame, sys

import config
from view.gameView import GameView
from view.menuView import MenuView
from controller.gameController import GameController
from controller.menuController import MenuController

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
pygame.display.set_caption("Interface de Jeu ACL ")
clock = pygame.time.Clock()

# Appels des classes dans les autres fichiers
menuView = MenuView(screen, sonClic)
gameView = GameView(screen, [], tailleRenduCase=config.tailleCaseRendu)
menuController = MenuController(menuView, sonClic)
gameController = GameController(gameView)

# Boucle principale
etat = "menu"
running = True
while running:
    dt = clock.tick(config.imageParSeconde) / 1000.0  # Temps écoulé depuis la dernière frame en secondes

    ancienneFenetre = etat

    # Gestion des event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if etat == "jeu":
            etat = gameController.gererEvenement(event)
        else:
            etat = menuController.gererEvenement(event, etat)

    if ancienneFenetre != etat and etat == "jeu":
        gameController.initialiserVariable(menuController.recupererDifficulte())

    # Gestion Update
    if etat == "jeu":
        gameController.updateJeu(dt)
    elif etat == "quitter":
        running = False

    # Gestion affichage
    if etat == "jeu":
        gameController.dessiner()
    else:
        menuController.dessiner(etat)

    pygame.display.flip()

pygame.quit()
sys.exit()

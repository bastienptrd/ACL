import os
import random
import pygame
import config

sons = {}
# Canaux réservés : un seul son à la fois sur chacun, donc pas de superposition
CANAL_MONSTRE, CANAL_SORTIE, CANAL_HASARD = 0, 1, 2
cible = None  # monstre que l'on entend


def charger() -> None:
    pygame.mixer.set_num_channels(16)
    pygame.mixer.set_reserved(3)
    for fichier in os.listdir(config.sons_jeu_path):
        sons[fichier.removesuffix(".wav")] = pygame.mixer.Sound(os.path.join(config.sons_jeu_path, fichier))


def cote(joueur, source) -> float:
    # -1 : la source est à gauche, 0 : en face ou derrière, 1 : à droite
    ecart = source.getPosition() - joueur.getPosition()
    return ecart.x / ecart.length() if ecart.length() > 0.1 else 0


def regler(canal, volume : float, cote : float) -> None:
    canal.set_volume(volume * min(1, 1 - cote), volume * min(1, 1 + cote))


def jouer(nom : str, volume : float = 1, cote : float = 0) -> None:
    if nom in ("mort", "victoire"):
        pygame.mixer.stop()
    sons[nom].set_volume(config.volumeClic)
    sons[nom].stop()  # un même son ne se superpose pas à lui-même
    canal = sons[nom].play()
    if canal:
        regler(canal, volume, cote)


def repeter(nom : str, volume : float = 1, cote : float = 0) -> None:
    # À appeler à chaque frame : relance le son seulement quand il est terminé
    if sons[nom].get_num_channels() == 0:
        jouer(nom, volume, cote)


def localiser(numero : int, nom : str, joueur, source) -> None:
    # À appeler à chaque frame : le son suit la source (gauche / droite et distance)
    canal = pygame.mixer.Channel(numero)
    volume = 1 - joueur.getPosition().distance_to(source.getPosition()) / config.distanceSon
    if volume <= 0:
        canal.stop()
        return
    if not canal.get_busy():
        sons[nom].set_volume(config.volumeClic)
        canal.play(sons[nom])
    regler(canal, volume, cote(joueur, source))


def jouerSonsJeu(joueur, ennemis : list, fin) -> None:
    # Sons continus qui informent le joueur sur son état et ce qui l'entoure
    global cible
    vie = joueur.health / joueur.healthMax
    if vie <= 0.25:
        repeter("coeur_rapide")
    elif vie <= 0.5:
        repeter("coeur")
    if joueur.opacite <= config.opaciteMax * 0.4:
        repeter("lampe_faible")
    localiser(CANAL_SORTIE, "sortie", joueur, fin)

    # On entend seulement le monstre vivant le plus proche
    monstre, hasard = pygame.mixer.Channel(CANAL_MONSTRE), pygame.mixer.Channel(CANAL_HASARD)
    if cible and cible.estMort():
        monstre.stop()
    if not monstre.get_busy():
        vivants = [ennemi for ennemi in ennemis if not ennemi.estMort()]
        cible = min(vivants, key=lambda ennemi: ennemi.getPosition().distance_to(joueur.getPosition()), default=None)
    if cible:
        localiser(CANAL_MONSTRE, cible.name, joueur, cible)

    # Bruits d'ambiance au hasard, coupés dès qu'un monstre est proche
    if monstre.get_busy():
        hasard.fadeout(500)
    elif not hasard.get_busy() and random.random() < 1 / (config.tempsEntreBruits * config.imageParSeconde):
        bruit = sons[random.choice([nom for nom in sons if nom.startswith("hasard_")])]
        bruit.set_volume(config.volumeClic * config.volumeBruits)
        hasard.play(bruit)

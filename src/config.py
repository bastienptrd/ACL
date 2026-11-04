import os
import pygame

#region CHEMIN
assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
images_path = os.path.join(assets_path, "images")
boutons_path = os.path.join(images_path, "Bouton")
sounds_path = os.path.join(assets_path, "sounds")
#endregion

#region BARRE DE VIE
barre_vie_path = os.path.join(images_path, "Barre_de_vie")
barre_vie_images = {
    25:  os.path.join(barre_vie_path, "Barre_de_vie_25.png"),
    50:  os.path.join(barre_vie_path, "Barre_de_vie_50.png"),
    75:  os.path.join(barre_vie_path, "Barre_de_vie_75.png"),
    100: os.path.join(barre_vie_path, "Barre_de_vie_100.png"),
}
barreVieLargeur = 300
barreViePosition = (700, 600)
#endregion

#region EVENEMENTS
EVENT_DEGATS = pygame.USEREVENT + 1   # événement personnalisé "le joueur prend des dégâts"
toucheTestDegats = pygame.K_k         # touche de test
degatsTest = 25
#endregion

#region IMAGES
player_img_path = os.path.join(images_path, "character", "test_img.png")
fond_menu_path = os.path.join(boutons_path, "foret_pixel.png")
bouton_jouer_path = os.path.join(boutons_path, "JOUER_1.png")
bouton_quitter_path = os.path.join(boutons_path, "QUITTER_1.png")
bouton_parametre_path = os.path.join(boutons_path, "PARAMETRE_1.png")
bouton_audio_path = os.path.join(boutons_path, "AUDIO_2.png")
bouton_commande_path = os.path.join(boutons_path, "COMMANDE_2.png")
bouton_gameplay_path = os.path.join(boutons_path, "GAMEPLAY_2.png")
#endregion

#region SONS
musique_foret_path = os.path.join(sounds_path, "Bruit_foret.mp3")
son_clic_path = os.path.join(sounds_path, "clic_2.wav")

volumeFond = 0.5
volumeClic = 1
#endregion


#region CONSTANTE
#region FENETRE
screenSize = (1080, 720)
imageParSeconde = 60

#endregion


#region PLAYER
vitesseJoueur = 2
vieJoueur = 100
tailleCollisionJoueur = (0.2, 0.2)
tailleCollisionFin = (0.1, 0.1)
#endregion

#region BULLET
vitesseBullet = 5
#endregion

#region RENDU
tailleCaseRendu = (500, 500)
tailleCharacter = (64, 50)
tailleBullet =(100,100)
#endregion

#region MAZE
nombreObstacle = 5
nombreApparitionEnemi = 5

# Case
caseVide = 0
caseMur = -1
caseDebut = -2
caseFin = -3
caseObstacle = -4
caseApparitionEnemi = -5
#endregion

#endreion

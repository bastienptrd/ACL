import os

# Chemins des assets, calculés depuis l'emplacement de ce fichier
# pour fonctionner sur n'importe quelle machine
assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
images_path = os.path.join(assets_path, "images")
boutons_path = os.path.join(images_path, "Bouton")
sounds_path = os.path.join(assets_path, "sounds")

# Images
player_img_path = os.path.join(images_path, "character", "test_img.png")
fond_menu_path = os.path.join(boutons_path, "foret_pixel.png")
bouton_jouer_path = os.path.join(boutons_path, "JOUER_1.png")
bouton_quitter_path = os.path.join(boutons_path, "QUITTER_1.png")
bouton_parametre_path = os.path.join(boutons_path, "bouton_parametre.png")
bouton_audio_path = os.path.join(boutons_path, "AUDIO_1.png")
bouton_commande_path = os.path.join(boutons_path, "COMMANDE_1.png")
bouton_gameplay_path = os.path.join(boutons_path, "GAMEPLAY_1.png")

# Sons
musique_foret_path = os.path.join(sounds_path, "Bruit_foret.mp3")
son_clic_path = os.path.join(sounds_path, "clic_2.wav")

#Constante
# Labyrinthe
# Case
mur = -1
debut = -2
fin = -3
obstacle = -4
apparitionEnemi = -5

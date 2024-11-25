import pygame
from game import Game  # Assurez-vous que le fichier "game.py" contient la classe Game

# Initialisation des modules Pygame
pygame.init()
pygame.font.init()

# Création de la fenêtre
pygame.display.set_caption("Menu interactif")
screen = pygame.display.set_mode((1080, 720))

# Chargement de l'arrière-plan
arriere_plan = pygame.image.load("image/ecran_titre.JPG")
arriere_plan = pygame.transform.scale(arriere_plan, (1080, 720))

# Chargement de la musique
music = pygame.mixer.Sound('musique/ambiance.mp3')
music.play(loops=-1)  # Répéter la musique en boucle
music.set_volume(0.1)

# Couleurs
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)

# Initialisation de la police
font = pygame.font.Font("acadian_runes/police.ttf", 80)  

# Initialisation de la police pour les crédits (pour que le texte soit plus petit)
font_credit = pygame.font.Font("acadian_runes/police.ttf", 40)  

# Options du menu
options = ["Jouer", "Son", "Crédit","Quitter"]
selected_option = 0  # Index de l'option sélectionnée

# Options pour la sélection des personnages
options_perso = ["2 joueurs", "3 joueurs","retour"]

#options_son 
options_son =["Activer", "Désactiver","retour"]

#option credit
options_credit =["retour"]

# Définition de la scène en cours
scene_courant = "Menu principal"

# Le texte des crédits, divisé en plusieurs lignes
credit_text = [
    "Jeu créé pour un projet de cours",
    "Développé par :",
    "Nos noms",  
]

# Création d'une instance du jeu
game = Game()

# Boucle principale
running = True
while running:
    # Afficher l'image d'arrière-plan
    screen.blit(arriere_plan, (0, 0))

    if scene_courant == "Menu principal":
        # Afficher les options principales
        for i, option in enumerate(options):
            color = ROUGE if i == selected_option else BLANC  # Rouge si sélectionné, blanc sinon
            texte = font.render(option, True, color)
            text_rect = texte.get_rect(center=(540, 300 + i * 90))  # Espacement vertical entre les options
            screen.blit(texte, text_rect.topleft)

    elif scene_courant == "selection_perso":
        # Afficher les options pour la sélection du nombre de joueurs
        for i, option in enumerate(options_perso):
            color = ROUGE if i == selected_option else BLANC  # Rouge si sélectionné, blanc sinon
            texte = font.render(option, True, color)
            text_rect = texte.get_rect(center=(540, 300 + i * 90))  # Espacement vertical entre les options
            screen.blit(texte, text_rect.topleft)

    elif scene_courant == "Menu son":
        # Afficher les options pour la sélection du nombre de joueurs
        for i, option in enumerate(options_son):
            color = ROUGE if i == selected_option else BLANC  # Rouge si sélectionné, blanc sinon
            texte = font.render(option, True, color)
            text_rect = texte.get_rect(center=(540, 300 + i * 90))  # Espacement vertical entre les options
            screen.blit(texte, text_rect.topleft)

    elif scene_courant == "Credit":
        #affiché les crédits : 
        y_offset = 250  # Position de départ pour les crédits
        for line in credit_text:
            texte = font_credit.render(line, True, BLANC)
            text_rect = texte.get_rect(center=(540, y_offset))  
            screen.blit(texte, text_rect.topleft)
            y_offset += 60  

        # Afficher les options pour la sélection du nombre de joueurs
        for i, option in enumerate(options_credit):
            color = ROUGE if i == selected_option else BLANC  # Rouge si sélectionné, blanc sinon
            texte = font.render(option, True, color)
            text_rect = texte.get_rect(center=(540, 600 ))  # Espacement vertical entre les options
            screen.blit(texte, text_rect.topleft)


    # Mettre à jour l'écran
    pygame.display.flip()

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du menu")

        # Détection des touches
        if scene_courant == "Menu principal":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Flèche bas
                    selected_option = (selected_option + 1) % len(options)  # Passer à l'option suivante
                elif event.key == pygame.K_UP:  # Flèche haut
                    selected_option = (selected_option - 1) % len(options)  # Revenir à l'option précédente
                elif event.key == pygame.K_RETURN:  # Touche Entrée
                    if selected_option == 0:  # Option "Jouer"
                        scene_courant = "selection_perso"
                    elif selected_option == 1:  #pour regler le sons, si on l'active ou non 
                        scene_courant = "Menu son"
                    elif selected_option == 2: #pour afficher les credit
                        scene_courant = "Credit"

                    elif selected_option == 3:  # Option "Quitter"
                        print("Jeu quitté !")
                        running = False
                        pygame.quit()

        elif scene_courant == "selection_perso":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Flèche bas
                    selected_option = (selected_option + 1) % len(options_perso)  # Passer à l'option suivante
                elif event.key == pygame.K_UP:  # Flèche haut
                    selected_option = (selected_option - 1) % len(options_perso)  # Revenir à l'option précédente
                elif event.key == pygame.K_RETURN:  # Touche Entrée
                    if selected_option == 0:  # Nombre de joueurs est 2
                        game.nombre_joueur = 2
                    elif selected_option == 1:  # Nombre de joueurs est 3
                        game.nombre_joueur = 3
                    elif selected_option == 2 : 
                        scene_courant = "Menu principal"

        elif scene_courant == "Menu son":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Flèche bas
                    selected_option = (selected_option + 1) % len(options_perso)  # Passer à l'option suivante
                elif event.key == pygame.K_UP:  # Flèche haut
                    selected_option = (selected_option - 1) % len(options_perso)  # Revenir à l'option précédente
                elif event.key == pygame.K_RETURN:  # Touche Entrée
                    if selected_option == 0:  # activer le son
                        music.set_volume(0.1)
                    elif selected_option == 1:  #desactiver le son 
                        music.set_volume(0.)
                    elif selected_option == 2 : 
                        scene_courant = "Menu principal"
        elif scene_courant == "Credit":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Flèche bas
                    selected_option = (selected_option + 1) % len(options_perso)  # Passer à l'option suivante
                elif event.key == pygame.K_UP:  # Flèche haut
                    selected_option = (selected_option - 1) % len(options_perso)  # Revenir à l'option précédente
                elif event.key == pygame.K_RETURN:  # Touche Entrée
                    if selected_option == 0:  # retour en arrière
                        scene_courant = "Menu principal"
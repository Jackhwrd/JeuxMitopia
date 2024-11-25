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

# Couleurs
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)

# Initialisation de la police
font = pygame.font.Font("acadian_runes/police.ttf", 80)  

# Options du menu
options = ["Jouer", "Quitter"]
selected_option = 0  # Index de l'option sélectionnée

# Options pour la sélection des personnages
options_perso = ["2 joueurs", "3 joueurs"]

# Définition de la scène en cours
scene_courant = "Menu principal"

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
                    elif selected_option == 1:  # Option "Quitter"
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
                        print("Nombre de joueurs est 2")
                        running = False  # Remplacer par une fonction pour démarrer le jeu
                    elif selected_option == 1:  # Nombre de joueurs est 3
                        game.nombre_joueur = 3
                        print("Nombre de joueurs est 3")
                        running = False  # Remplacer par une fonction pour démarrer le jeu
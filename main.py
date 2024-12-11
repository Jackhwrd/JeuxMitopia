import pygame
from game import *  
from unit import *
from image import *

# Initialisation des modules Pygame
pygame.init()
pygame.font.init()

# Création de la fenêtre
pygame.display.set_caption("Menu interactif")
screen = pygame.display.set_mode((1080, 720))

# Chargement de l'arrière-plan

arriere_plan = pygame.transform.scale(arriere_plan, (1080, 720))


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
    "Jack HOWARD",
    "Camilia ZARKI",
    "Djahane ESCUDIE",
    "musique : 8 bit donjon de Kaden_Cook sur pixabay ",
    "police d'écriture : Acadian Runes sur dafont.com"
]

#choix des perso : 
list_joueur = ["Croque - Minou","Guts","Batorie","Menue principal"]
#chargement des images et redimmensionnement pour le menu de selection


nouvelle_largeur = 100 
nouvelle_hauteur = 100  
new_croque_minou = pygame.transform.scale(image_croque_minou, (nouvelle_largeur, nouvelle_hauteur))

image_vide = pygame.Surface((1, 1), pygame.SRCALPHA)
image_vide.fill((0, 0, 0, 0))  # Remplir avec une transparence complète (RGBA : alpha = 0)

list_image = [
    new_croque_minou,
    new_croque_minou,
    new_croque_minou,
    image_vide
]
# Chargement de la musique
music = pygame.mixer.Sound('musique/ambiance.mp3')
music.play(loops=-1)  
music.set_volume(0.1)


# Boucle principale
running = True
while running:
    # Afficher l'image d'arrière-plan
    screen.blit(arriere_plan, (0, 0))

    if scene_courant == "Menu principal":
        
        #initialisation du choix des personnages
        player_classe = []
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
        y_offset = 210  # Position de départ pour les crédits
        for line in credit_text:
            text_rect = texte.get_rect(center=(540, y_offset))  
            screen.blit(texte, text_rect.topleft)
            y_offset += 50  

        # Afficher les options pour la sélection du nombre de joueurs
        for i, option in enumerate(options_credit):
            color = ROUGE if i == selected_option else BLANC  # Rouge si sélectionné, blanc sinon
            texte = font.render(option, True, color)
            text_rect = texte.get_rect(center=(540, 600 ))  # Espacement vertical entre les options
            screen.blit(texte, text_rect.topleft)

    elif scene_courant == "selection_perso1":
        texte = font.render("Joueur 1 choisie ton perso", True, BLANC)
        text_rect = texte.get_rect(center=(540, 210 ))
        screen.blit(texte, text_rect.topleft)
        for i, option in enumerate(list_joueur):
            color = ROUGE if i == selected_option else BLANC  # Rouge si sélectionné, blanc sinon
            texte = font.render(option, True, color)
            text_rect = texte.get_rect(center=(540, 300 + i * 110))  # Espacement vertical entre les options
            screen.blit(texte, text_rect.topleft)

            image = list_image[i]
            image_rect = image.get_rect(midleft=(text_rect.right + 20, text_rect.centery))  # Décale l'image à droite du texte
            screen.blit(image, image_rect.topleft)

    elif scene_courant == "selection_perso2":
        texte = font.render("Joueur 2 choisie ton perso", True, BLANC)
        text_rect = texte.get_rect(center=(540, 210 ))
        screen.blit(texte, text_rect.topleft)
        for i, option in enumerate(list_joueur):
            color = ROUGE if i == selected_option else BLANC  # Rouge si sélectionné, blanc sinon
            texte = font.render(option, True, color)
            text_rect = texte.get_rect(center=(540, 300 + i * 110))  # Espacement vertical entre les options
            screen.blit(texte, text_rect.topleft)

            image = list_image[i]
            image_rect = image.get_rect(midleft=(text_rect.right + 20, text_rect.centery))  # Décale l'image à droite du texte
            screen.blit(image, image_rect.topleft)
        
    elif scene_courant == "selection_perso3":
        texte = font.render("Joueur 3 choisie ton perso", True, BLANC)
        text_rect = texte.get_rect(center=(540, 210 ))
        screen.blit(texte, text_rect.topleft)
        for i, option in enumerate(list_joueur):
            color = ROUGE if i == selected_option else BLANC  # Rouge si sélectionné, blanc sinon
            texte = font.render(option, True, color)
            text_rect = texte.get_rect(center=(540, 300 + i * 110))  # Espacement vertical entre les options
            screen.blit(texte, text_rect.topleft)

            image = list_image[i]
            image_rect = image.get_rect(midleft=(text_rect.right + 20, text_rect.centery))  # Décale l'image à droite du texte
            screen.blit(image, image_rect.topleft)


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
                        scene_courant = "selection_perso1"
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
                    
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        pygame.display.set_caption("Mon jeu de stratégie")
                        game = Game(screen,2)
                        In_Game = True
                        while In_Game:
                            game.handle_player_turn()
                            game.handle_enemy_turn()
                            #if event.type == pygame.Keydown:
                            
                    elif selected_option == 1:  # Nombre de joueurs est 3
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        pygame.display.set_caption("Mon jeu de stratégie")
                        game = Game(screen,3)
                        In_Game = True
                        while True:
                            game.handle_player_turn()
                            game.handle_enemy_turn()
                            #if event.type
                            
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

        elif scene_courant == "selection_perso1":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Flèche bas
                    selected_option = (selected_option + 1) % len(list_joueur)  # Passer à l'option suivante
                elif event.key == pygame.K_UP:  # Flèche haut
                    selected_option = (selected_option - 1) % len(list_joueur)  # Revenir à l'option précédente
                elif event.key == pygame.K_RETURN:  # Touche Entrée
                    if selected_option == 0:  #choix du mage
                        player_classe.append(("Mage"))
                        scene_courant = "selection_perso2"
                    elif selected_option == 1:  #choix du guerrier
                        player_classe.append("Guerrier")
                        scene_courant = "selection_perso2"
                    elif selected_option == 2:  #choix du vampire
                        player_classe.append("Vampire")
                        scene_courant = "selection_perso2"
                    elif selected_option == 3 :
                        scene_courant = "Menu principal"

        
        elif scene_courant == "selection_perso2":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Flèche bas
                    selected_option = (selected_option + 1) % len(list_joueur)  # Passer à l'option suivante
                elif event.key == pygame.K_UP:  # Flèche haut
                    selected_option = (selected_option - 1) % len(list_joueur)  # Revenir à l'option précédente
                elif event.key == pygame.K_RETURN:  # Touche Entrée
                    if selected_option == 0:  
                        player_classe.append("Mage")
                        scene_courant = "selection_perso3"
                    elif selected_option == 1:  
                        player_classe.append("Guerrier")
                        scene_courant = "selection_perso3"
                    elif selected_option == 2:  
                        player_classe.append("Vampire")
                        scene_courant = "selection_perso3"
                    elif selected_option == 3 :
                        scene_courant = "Menu principal"

        elif scene_courant == "selection_perso3":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Flèche bas
                    selected_option = (selected_option + 1) % len(list_joueur)  # Navigue dans `list_joueur`
                elif event.key == pygame.K_UP:  # Flèche haut
                        selected_option = (selected_option - 1) % len(list_joueur)  # Navigue dans `list_joueur`
                elif event.key == pygame.K_RETURN:  # Touche Entrée
                    if selected_option == 0:  
                        player_classe.append("Mage")
                        game = Game(screen,3,player_classe)
                        In_Game = True
                        while True:
                            game.handle_player_turn()
                            game.handle_enemy_turn()
                    elif selected_option == 1:  
                        player_classe.append("Guerrier")
                        game = Game(screen,3,player_classe)
                        In_Game = True
                        while True:
                            game.handle_player_turn()
                            game.handle_enemy_turn()
                    elif selected_option == 2:  
                        player_classe.append("Vampire")
                        game = Game(screen,3,player_classe)
                        In_Game = True
                        while True:
                            game.handle_player_turn()
                            game.handle_enemy_turn()
                    elif selected_option == 3 :
                        scene_courant = "Menu principal"
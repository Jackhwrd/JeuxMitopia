import pygame 
import random

from unit import *
from game_map import *
from image import *
from classes import *

walls = mur()
rooms = generate_rooms(salles)


class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """
    

    def __init__(self, screen, player_count,player_classe):
        """
        Initialise le jeu avec les paramètres nécessaires.
        """
        self.screen = screen
        self.enemy_images = [image_mechant_guerier, image_mechant_vampire, image_mechant_mage]
        self.player_class = player_classe # liste des classes des joueurs 

        self.walls = mur()
        self.salles = salles
        self.rooms = generate_rooms(salles)
        self.objects = generate_objects()

        self.player_units = []
        for i, player_class in enumerate(player_classe):
            if player_class == "Mage":
                    self.player_units.append(Mage_player(i,0))
            elif player_class == "Vampire":
                    self.player_units.append(Vampire_player(i,0))
            elif player_class == "Guerrier":
                    self.player_units.append(Guerrier_player(i,0))


        self.enemy_units = [Vampire_enemy(6,6),
                            Vampire_enemy(7,6),
                            Vampire_enemy(8,6)]

        # Prépare les rectangles pour les cellules de la grille
        self.grid_rects = [
            pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            for x in range(0, WIDTH, CELL_SIZE)
            for y in range(0, HEIGHT, CELL_SIZE)
        ]

                
    def handle_player_turn(self):
        """Tour du joueur"""
        for rang_joueur, selected_unit in enumerate (self.player_units):

                

                # Tant que l'unité n'a pas terminé son tour
                has_acted = False
                selected_unit.is_selected = True
                selecting_attack = False  # Flag pour savoir si on est dans le menu d'attaque
                current_option = 0  # Option actuelle
                selected_attack = 0  # Attaque actuellement sélectionnée
                self.flip_display()
                
                while not has_acted: # tant que le tour du joueur n'est pas fini
                    #affichage du numéros de joueur qui doit jouer 

                    phrase = f"Joueur {rang_joueur + 1 }, à toi de jouer !"
                    texte = font_affi_joueur.render(phrase, True, WHITE)
                    text_rect = texte.get_rect(center=(540, 20))  # Espacement vertical entre les options
                    self.screen.blit(texte, text_rect.topleft)
                    

                    # Boucle principale d'événements
                    for event in pygame.event.get():
                        # Gestion de la fermeture de la fenêtre
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()

                        # Gestion des touches du clavier
                        if event.type == pygame.KEYDOWN:
                            # Si on n'est pas dans le menu d'attaque, afficher les options principales
                            if not selecting_attack:
                                # Déplacement du curseur entre "Avancer" et "Attaquer"
                                if event.key == pygame.K_DOWN:
                                    current_option = (current_option + 1) % 2
                                elif event.key == pygame.K_UP:
                                    current_option = (current_option - 1) % 2
                                
                                # Si l'option "Attaquer" est sélectionnée
                                if event.key == pygame.K_RETURN and current_option == 1:
                                    selecting_attack = True  # On passe dans le menu d'attaque
                                    self.flip_display(attacking=False, Attack=None)

                                # Si l'option "Avancer" est sélectionnée, on déplace l'unité
                                if event.key == pygame.K_RETURN and current_option == 0:
                                    self.move_unit_multiple(selected_unit)
                                    self.flip_display(attacking=False, Attack=None)
                                    has_acted = True 
                                
                            # Si on est dans le menu d'attaque
                            else:
                                # Sélection des attaques
                                if event.key == pygame.K_DOWN:
                                    selected_attack = (selected_attack + 1) % len(selected_unit.liste_attaque)
                                elif event.key == pygame.K_UP:
                                    selected_attack = (selected_attack - 1) % len(selected_unit.liste_attaque)

                                # Si l'attaque est confirmée
                                if event.key == pygame.K_RETURN:
                                    
                                    if selected_attack == 0:  
                                        
                                        selected_unit.attaque(selected_unit.liste_attaque[0],self)
                                    elif selected_attack == 1:  
                                        selected_unit.attaque(selected_unit.liste_attaque[1],self)
                                    elif selected_attack == 2 : 
                                        selected_unit.attaque(selected_unit.liste_attaque[0],self)
                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:

                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                            if selected_unit.x == 0 and selected_unit.y == GRID_SIZE_V - 1:
                                target_pos = (GRID_SIZE_H - 1, 0)  # Par exemple, coordonnées de téléportation
                                teleport_unit(selected_unit, target_pos, self.rooms, self.salles)
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                            # Téléportation si en haut à droite
                            if selected_unit.x == GRID_SIZE_H - 1 and selected_unit.y == 0:
                                target_pos = (0, GRID_SIZE_V - 1)  # Par exemple, coordonnées de téléportation
                                teleport_unit(selected_unit, target_pos, self.rooms, self.salles)
                                #self.flip_display()
                                #has_acted = True
                                continue
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
                        
                        new_x = selected_unit.x + dx
                        new_y = selected_unit.y + dy
                        if not (0 <= new_x < GRID_SIZE_H and 0 <= new_y < GRID_SIZE_V):
                            print("Vous ne pouvez pas sortir des limites de la carte !")
                            continue

                        # Si la touche entrer est appuyée, essayer de ramasser un objet
                        if event.key == pygame.K_RETURN:  # Touche entrer du pavé numérique
                            for obj in self.objects:
                                if obj.x == selected_unit.x and obj.y == selected_unit.y:
                                    print(f"Vous avez ramassé {obj.name} !")
                                    obj.collected = True  # L'objet est ramassé
                                    self.objects.remove(obj)  # Retirer de la carte
                                    
                                    # Ajoutez l'objet à la liste `has_object` (si elle existe, sinon initialisez-la)
                                    if not hasattr(selected_unit, 'has_object'):
                                        selected_unit.has_object = []  # Si la liste n'existe pas, créez-la

                                    selected_unit.has_object.append(obj)  # Ajouter l'objet à la liste
                                    print(f"L'objet dans has_object : {selected_unit.has_object[-1].name}")  # Affiche le dernier objet collecté
                                    break 

                        # Vérifier les collisions avec les murs
                        proposed_rect = pygame.Rect(
                            new_x * CELL_SIZE,
                            new_y * CELL_SIZE,
                            CELL_SIZE,
                            CELL_SIZE,
                        )
                        if any(proposed_rect.colliderect(wall) for wall in self.walls):
                            print("Collision détectée ! Mouvement annulé.")
                            # Collision détectée : ne pas appliquer le déplacement
                            continue

                        # Vérifier si le joueur tente d'entrer dans une salle
                        room_id = (
                            self.rooms[new_x, new_y]
                            if (0 <= new_x < GRID_SIZE_H and 0 <= new_y < GRID_SIZE_V)
                            else 0
                        )
                        salle = next((s for s in salles if s.id == room_id), None)

                        # Si la salle est ouverte
                        if salle:
                            if salle.verifier_conditions(selected_unit):
                                selected_unit.x, selected_unit.y = new_x, new_y
                                print(f"Vous êtes entré dans la salle {salle.id}.")
                            else:
                                print(f"Accès refusé à la salle {salle.id}.")

                        # Si le joueur entre dans une salle, vérifier les conditions
                        if salle:
                            if salle.verifier_conditions(selected_unit):
                                selected_unit.x, selected_unit.y = new_x, new_y
                                print(f"Vous êtes entré dans la salle {salle.id}.")
                            else:
                                print(f"Accès refusé à la salle {salle.id}.")
                        else:
                            # Pas de salle : déplacer normalement
                            selected_unit.x, selected_unit.y = new_x, new_y
                            
                        self.flip_display()
                        # Attaque (touche espace) met fin au tour
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

                                    has_acted = True
                                    selected_unit.is_selected = False

                    # Affichage des options principales (Avancer ou Attaquer)
                    if not selecting_attack:
                        options = ["Avancer", "Attaquer"]
                        for i, option in enumerate(options):
                            color = BLUE if i == current_option else WHITE
                            texte = font.render(option, True, color)
                            text_rect = texte.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 70))
                            self.screen.blit(texte, text_rect)
                    
                    # Affichage des attaques si l'option "Attaquer" est choisie
                    else:
                        for i, attack in enumerate(selected_unit.liste_attaque):
                            color = BLUE if i == selected_attack else WHITE
                            texte = font.render(attack, True, color)
                            text_rect = texte.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 70))
                            self.screen.blit(texte, text_rect)

                    # Mise à jour de l'affichage
                    pygame.display.flip()

         

        


    
    def move_unit_multiple(self, unit):
        """Permet au joueur de déplacer l'unité vers une position cible."""
        target_x, target_y = unit.x, unit.y  # Position actuelle
        while True:
            # Afficher la grille avec la position cible surlignée
            self.flip_display(attacking=False, Attack=None)
            highlight_rect = pygame.Rect(target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, YELLOW, highlight_rect, 3)  # Surligne la position cible
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1

                    # Mettre à jour la position cible
                    new_x, new_y = target_x + dx, target_y + dy
                    # Vérification si la nouvelle position est valide (pas un mur)
                    if 0 <= new_x < GRID_SIZE_H and 0 <= new_y < GRID_SIZE_V and not self.is_wall(new_x, new_y):
                        target_x, target_y = new_x, new_y

                    # Valider le déplacement
                    if event.key == pygame.K_RETURN:
                        unit.x, unit.y = target_x, target_y
                        return

    def is_wall(self, x, y):
        """Vérifie si une case donnée contient un mur."""
        for wall in walls:
            if wall.collidepoint(x * CELL_SIZE, y * CELL_SIZE):
                return True
        return False
    
    def is_occupied_by_unit(self, x, y):
        """Vérifie si une case est occupée par une unité."""
        for unit in self.player_units + self.enemy_units:
            if unit.x == x and unit.y == y:
                return True
        return False

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:
            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            
            new_x, new_y = enemy.x + dx, enemy.y + dy
            if 0 <= new_x < GRID_SIZE_H and 0 <= new_y < GRID_SIZE_V and not self.is_wall(new_x, new_y):
                enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)


    def move_unit_multiple(self, unit):
        """Permet au joueur de déplacer l'unité vers une position cible."""
        target_x, target_y = unit.x, unit.y  # Position actuelle
        while True:
            # Afficher la grille avec la position cible surlignée
            self.flip_display(attacking=False, Attack=None)
            highlight_rect = pygame.Rect(target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, YELLOW, highlight_rect, 3)  # Surligne la position cible
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1

                    # Mettre à jour la position cible
                    new_x, new_y = target_x + dx, target_y + dy

                    # Vérification si la nouvelle position est valide (pas un mur et pas occupée par une autre unité)
                    if 0 <= new_x < GRID_SIZE_H and 0 <= new_y < GRID_SIZE_V and not self.is_wall(new_x, new_y) and not self.is_occupied_by_unit(new_x, new_y):
                        target_x, target_y = new_x, new_y

                    # Valider le déplacement
                    if event.key == pygame.K_RETURN:
                        unit.x, unit.y = target_x, target_y
                        return

    def flip_display(self, attacking=False, Attack=None):
        """Affiche le jeu."""

        # Effacer l'écran (en dehors de la boucle principale pour éviter les flashs)
        self.screen.fill(RED)

        # Affiche la grille
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                
                # Obtenir la couleur de la cellule
                color = get_cell_color(grid_x, grid_y, self.rooms, self.walls, salles)
                    
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect)

                # Ne pas dessiner la grille pour les cases de murs
                if self.is_wall(grid_x, grid_y):
                    pygame.draw.rect(self.screen, BLACK, rect)  # Dessiner les murs

                pygame.draw.rect(self.screen, BLACK, rect, 1) #grille

        # Affiche les objets
        for obj in self.objects:
            obj.draw(self.screen)

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)
            unit.update_health_bar(self.screen)

        # Affiche les objets
        for obj in self.objects:
            obj.draw(self.screen)
        
        # Afficher les attaques si nécessaire
        if attacking:
            Attack.draw(self.screen)

        # Rafraîchissement de l'écran
        pygame.display.flip()

    def game_over() :
        pass 
        
    def victoire() : 
        pass


def main():

    # Initialisation de Pygame
    #pygame.init()
    #clock = pygame.time.Clock()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Test du jeu de stratégie")

    # Instanciation du jeu
    Perso = ["Mage","Guerrier","Vampire"]
    game = Game(screen, None, Perso)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()
        
if __name__ == "__main__":
    main()
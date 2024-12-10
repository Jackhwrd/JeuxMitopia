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

        self.player_units = []
        for i, player_class in enumerate(player_classe):
            if player_class == "Mage":
                    self.player_units.append(Mage_player(0, i, 10, 3, image_croque_minou, 2, 5))
            elif player_class == "Vampire":
                    self.player_units.append(Vampire_player(0, i, 8, 4, image_croque_minou, 3, 6))
            elif player_class == "Guerrier":
                    self.player_units.append(Guerrier_player(0, i, 12, 2, image_croque_minou, 4, 4))


        self.enemy_units = [Unit(6, 6, 8, 1, 'enemy',"Vampire",0,0),
                            Unit(7, 6, 8, 1, 'enemy',"Vampire",0,0),
                            Unit(8, 6, 8, 1, 'enemy',"Vampire",0,0)]
       

        # Associer les images des ennemis
        for unit, image in zip(self.enemy_units, self.enemy_images):
            unit.character_image = image

        # Prépare les rectangles pour les cellules de la grille
        self.grid_rects = [
            pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            for x in range(0, WIDTH, CELL_SIZE)
            for y in range(0, HEIGHT, CELL_SIZE)
        ]
        
        
    def handle_player_turn(self):
            """Tour du joueur : choix d'actions (déplacement ou attaque)."""
            for player_index, selected_unit in enumerate(self.player_units):
                has_acted = False
                selected_unit.is_selected = True
                current_option = 0  # 0 = Avancer, 1 = Attaquer
                selecting_attack = False  # False = choisir action, True = choisir attaque
                selected_attack = 0  # Index de l'attaque choisie (si applicable)

                while not has_acted:
                    # Efface l'écran et dessine le plateau de jeu
                    self.flip_display(attacking=False, Attack=None)

                    # Afficher un message pour le joueur actuel
                    joueur_text = f"Joueur {player_index + 1}, à toi de jouer !"
                    texte_joueur = font.render(joueur_text, True, WHITE)
                    self.screen.blit(texte_joueur, (WIDTH // 2 - 100, 20))

                    # Afficher les options principales (Avancer ou Attaquer)
                    if not selecting_attack:
                        options = ["Avancer", "Attaquer"]
                        for i, option in enumerate(options):
                            color = BLACK if i == current_option else WHITE
                            texte = font.render(option, True, color)
                            text_rect = texte.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
                            self.screen.blit(texte, text_rect)

                    # Afficher les attaques si le joueur choisit d'attaquer
                    else:
                        for i, attack in enumerate(selected_unit.liste_attaque):
                            color = BLACK if i == selected_attack else WHITE
                            texte = font.render(attack, True, color)
                            text_rect = texte.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
                            self.screen.blit(texte, text_rect)

                    pygame.display.flip()

                    # Gestion des événements
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()

                        if event.type == pygame.KEYDOWN:
                            # Navigation entre les options principales ou attaques
                            if event.key == pygame.K_UP:
                                if not selecting_attack:
                                    current_option = (current_option - 1) % 2
                                else:
                                    selected_attack = (selected_attack - 1) % len(selected_unit.liste_attaque)
                            elif event.key == pygame.K_DOWN:
                                if not selecting_attack:
                                    current_option = (current_option + 1) % 2
                                else:
                                    selected_attack = (selected_attack + 1) % len(selected_unit.liste_attaque)

                            # Validation du choix
                            if event.key == pygame.K_RETURN:
                                if not selecting_attack:
                                    if current_option == 0:  # Avancer
                                        print("Choix : Avancer")
                                        # Permet au joueur de déplacer l'unité
                                        self.move_unit_multiple(selected_unit)
                                        has_acted = True
                                    elif current_option == 1:  # Attaquer
                                        print("Choix : Attaquer")
                                        selecting_attack = True
                                else:
                                    print(f"Attaque choisie : {selected_unit.liste_attaque[selected_attack]}")
                                    # Effectue l'attaque (logique à implémenter)
                                    has_acted = True

                            # Annulation du choix d'attaque
                            if event.key == pygame.K_BACKSPACE and selecting_attack:
                                selecting_attack = False

                        # Limiter le nombre d'images par seconde
                        pygame.time.Clock().tick(FPS)


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
                    if 0 <= new_x < GRID_SIZE_H and 0 <= new_y < GRID_SIZE_V:
                        target_x, target_y = new_x, new_y

                    # Valider le déplacement
                    if event.key == pygame.K_RETURN:
                        unit.x, unit.y = target_x, target_y
                        return

    def move_unit(self, unit):
        """Déplacement de l'unité par le joueur."""
        while True:
            self.flip_display(attacking=False, Attack=None)
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

                    # Appliquer le déplacement si possible
                    unit.move(dx, dy)
                    self.flip_display(attacking=False, Attack=None)
                    return

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self,attacking,Attack):
        """Affiche le jeu."""
        
        # Affiche la grille
        self.screen.fill(RED)     
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
            
                # Obtenir la couleur de la cellule
                color = get_cell_color(grid_x, grid_y, rooms, walls, salles)
                    
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                pygame.draw.rect(self.screen, BLACK, rect, 1)

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)
        
        # Affiche les murs
        for wall in walls:
            pygame.draw.rect(self.screen, BLACK, wall)  # Dessiner les murs
              
        if attacking:
            Attack.draw(self.screen)
        
        # Rafraîchit l'écran
        pygame.display.flip()


def main():

    # Initialisation de Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    Perso = ["Mage","Guerrier","Vampire"]
    game = Game(screen,Perso)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()
        
if __name__ == "__main__":
    main()
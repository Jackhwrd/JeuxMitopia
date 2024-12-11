import pygame
import random
import numpy as np 

from unit import *
from game_map import *

class Game:
   
    def __init__(self, screen):
        
        self.screen = screen
        self.walls = mur()
        self.rooms = generate_rooms(salles)
        self.objects = generate_objects()

        self.player_units = [Unit(0, 0, 10, 2, 'player'),
                             Unit(1, 0, 10, 2, 'player'),
                             Unit(2, 0, 10, 2, 'player')]

        self.enemy_units = [Unit(6, 6, 8, 1, 'enemy'),
                            Unit(7, 6, 8, 1, 'enemy'),
                            Unit(8, 6, 8, 1, 'enemy')]
         
        # Prépare les rectangles pour les cellules de la grille
        self.grid_rects = [
            pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            for x in range(0, WIDTH, CELL_SIZE)
            for y in range(0, HEIGHT, CELL_SIZE)
        ]
        
    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:

                # Important: cette boucle permet de gérer les événements Pygame
                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:

                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                            # Téléportation si en haut à droite
                            if selected_unit.x == GRID_SIZE_H - 1 and selected_unit.y == 0:
                                teleport_unit(selected_unit, (0, GRID_SIZE_V - 1))
                                self.flip_display()
                                has_acted = True
                                continue
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
                        
                        new_x = selected_unit.x + dx
                        new_y = selected_unit.y + dy

                        # Si la touche + est appuyée, essayer de ramasser un objet
                        if event.key == pygame.K_KP_PLUS:  # Touche + du pavé numérique
                            for obj in self.objects:
                                if obj.x == selected_unit.x and obj.y == selected_unit.y:
                                    print(f"Vous avez ramassé {obj.name} !")
                                    obj.collected = True  # L'objet est ramassé
                                    self.objects.remove(obj)  # Retirer de la carte
                                    selected_unit.has_object = obj  # Associer l'objet à l'unité
                                    print(f"L'objet dans has_object : {selected_unit.has_object.name}")  # Debug
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

    def flip_display(self):
        """Affiche le jeu."""
        
        # Affiche la grille
        self.screen.fill(RED)     
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
            
                # Obtenir la couleur de la cellule
                color = get_cell_color(grid_x, grid_y, self.rooms, self.walls, salles)
                    
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                pygame.draw.rect(self.screen, BLACK, rect, 1)

        # Affiche les objets
        for obj in self.objects:
            obj.draw(self.screen)

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)
        
        # Affiche les murs
        for wall in self.walls:
            pygame.draw.rect(self.screen, BLACK, wall)  # Dessiner les murs
              
        
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
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()
        
if __name__ == "__main__":
    main()

import pygame
import random
import numpy as np 

from unit import *
from game_map import *

walls = mur()
rooms = generate_rooms(salles)

class Game:
   
    def __init__(self, screen,personnages):
        
        self.screen = screen
        self.perso = personnages
        self.player_units = [Unit(0, 0, 10, 2, 'player', personnages[0]),
                             Unit(1, 0, 10, 2, 'player', personnages[1]),
                             Unit(2, 0, 10, 2, 'player', personnages[2])]

        self.enemy_units = [Unit(6, 6, 8, 1, 'enemy',"Vampire"),
                            Unit(7, 6, 8, 1, 'enemy',"Vampire"),
                            Unit(8, 6, 8, 1, 'enemy',"Vampire")]
        
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
            attacking = False
            Attack = Attaque(NULL[0],NULL[1],NULL[2],NULL[3],NULL[4],NULL[5],NULL[6])
            self.flip_display(attacking,Attack)
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
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        if attacking == False:

                            selected_unit.move(dx,dy)

                            if selected_unit.x == GRID_SIZE_H - 1 and selected_unit.y == 0:
                                teleport_unit(selected_unit, (0, GRID_SIZE_V - 1))
                                self.flip_display(attacking,Attack)
                                dx, dy = 0,0
                                has_acted = True
                                selected_unit.is_selected = False
                                continue

                        elif attacking == True:
                            
                            Attack.move(dx,dy)

                            if abs(Attack.x - selected_unit.x) >= Attack.range or abs(Attack.y - selected_unit.y) >= Attack.range:
                                Attack.move(-dx,-dy)
                                                
                        if any(
                            pygame.Rect(
                                selected_unit.x * CELL_SIZE,
                                selected_unit.y * CELL_SIZE,
                                CELL_SIZE,
                                CELL_SIZE,
                            ).colliderect(wall)
                            for wall in walls
                        ):  
                                print("Collision détectée !")
                                # Annuler le mouvement si nécessaire
                                selected_unit.move(-dx, -dy)

                        #si un joueur appui sur une touche d'attaque
                        if (event.key == pygame.K_a) or (event.key == pygame.K_z) or (event.key == pygame.K_e) and not(attacking):
                            attacking = True
                            name, value, height, width, range= selected_unit.role.get_attacks()[event.key]
                            Attack = Attaque( name, value, height, width, range, selected_unit.x, selected_unit.y)
                            print("Attack ", name, "activé !")  #print le nom de l'attaque choisi

                        #appui sur une la touche espace pour annuler l'attaque
                        if (event.key == pygame.K_SPACE) and attacking:
                            Attack = Attaque(NULL[0],NULL[1],NULL[2],NULL[3],NULL[4],NULL[5],NULL[6])
                            attacking = False
                            print("attaque annulé")

                        
                        # Attaque (touche espace) met fin au tour
                        elif event.key == pygame.K_SPACE and not(attacking):
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)

                            has_acted = True
                            selected_unit.is_selected = False
                            
                        self.flip_display(attacking,Attack)

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

import pygame
import random

from unit import *
from game_map import *
from image import *
from classes import *

walls = mur()

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
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        selected_unit.move(dx, dy)
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
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, BLACK, rect, 1)

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)
        
        # Affiche les murs
        for wall in walls:
            pygame.draw.rect(self.screen, BLACK, wall)  # Dessiner les murs
        
        # Affiche le joueur
       # pygame.draw.rect(self.screen, (255, 0, 0), player)  # Dessiner le joueur

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
    game = Game(screen,3)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

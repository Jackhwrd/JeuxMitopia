import pygame
import random
from image import *

# Constantes
GRID_SIZE_V = 24
GRID_SIZE_H = 40
CELL_SIZE = 30
WIDTH = GRID_SIZE_H * CELL_SIZE
HEIGHT = GRID_SIZE_V * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)           #base RVB
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


# Constantes
GRID_SIZE_V = 24
GRID_SIZE_H = 40
CELL_SIZE = 30
WIDTH = GRID_SIZE_H * CELL_SIZE
HEIGHT = GRID_SIZE_V * CELL_SIZE
FPS = 30

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)           #base RVB
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
OLIVE = (128, 128, 0)
BROWN = (131, 118, 105)
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (255, 255, 153)
KAKI = (140, 130, 80)
MAGE = (182,37,207)
GUERRIER = (138,148,163)
VAMPIRE = (161,0,0)


class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, attack_power, team,image,defe,vit):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.character_image = image
        self.defense = defe
        self.vitess = vit

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE_H and 0 <= self.y + dy < GRID_SIZE_V:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else BLACK
   
        # Affiche le cadre vert si l'unité est sélectionnée
        
        # Affiche l'image du personnage
        if self.character_image:
            # Dessine l'image du personnage
            screen.blit(pygame.transform.scale(self.character_image, (CELL_SIZE, CELL_SIZE)),
                        (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
            # Optionnel : Affiche un cercle ou une couleur par défaut si aucune image n'est définie
            color = BLUE if self.team == 'player' else BLACK
            pygame.draw.circle(screen, color, 
                            (self.x * CELL_SIZE + CELL_SIZE // 2, 
                                self.y * CELL_SIZE + CELL_SIZE // 2), 
                            CELL_SIZE // 3)
import pygame
import random

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

class Unit:

    def __init__(self, x, y, health, attack_power, team, niveau=1):
        
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.niveau = niveau  # Niveau du joueur
        self.is_selected = False
        self.has_object = []

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
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
   
    def augmenter_niveau(self):
        self.niveau += 1
        print(f"Votre niveau a augmenté : {self.niveau}")

    def collect(self, obj):
        # Si l'objet n'est pas déjà dans la liste, on l'ajoute
        if obj.name not in [o.name for o in self.has_object]:
            self.has_object.append(obj)
            print(f"Vous avez ramassé : {obj.name}!")
        
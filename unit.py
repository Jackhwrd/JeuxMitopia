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
MAGE = (182,37,207)
GUERRIER = (138,148,163)
VAMPIRE = (161,0,0)
NULL = ("Null", 0, 0, 0, 0, 0)


class Role:
    def __init__(self,titre):
        self.__titre = titre 
    
    def get_titre(self):
        return self.__titre
        
    def get_attacks(self):
        if self.__titre == "Guerrier":
            attacks = {pygame.K_a : ("Slam", 2, 1, 1)}
        elif self.__titre == "Mage":
            attacks = {pygame.K_a : ("Fireball", 2, 1, 1)}
        elif self.__titre == "Vampire":
            attacks = {pygame.K_a : ("Drain", 2, 1, 1)}
        return attacks
    
class Attaque:
    def __init__(self, name, value, height, width, x, y):
        self.name = name
        self.value = value
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def draw(self,screen):
        pygame.draw.rect(screen, RED, (self.x * CELL_SIZE,self.y * CELL_SIZE, self.height * CELL_SIZE, self.width * CELL_SIZE))




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

    def __init__(self, x, y, health, attack_power, team, role):
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
        self.role = Role(role) 

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
        titre = self.role.get_titre()
        color = BLACK if self.team == 'enemy' else MAGE if titre == "Mage" else GUERRIER if titre == "Guerrier" else VAMPIRE
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                             self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
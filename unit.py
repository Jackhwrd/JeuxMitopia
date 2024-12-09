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
NULL = ("Null", 0, 0, 0, 0, 0, 0)
IMAGE = None
IMAGE_CROQUE_MINOU = None
IMAGE_MECHANT_MAGE = None
IMAGE_MECHANT_GUERRIER = None
IMAGE_MECHANT_VAMPIRE = None
IMAGE_ROI = None
IMAGE_STATUS = None



class Role:
    def __init__(self,titre):
        self.__titre = titre 
    
    def get_titre(self):
        return self.__titre
        
    def get_attacks(self):
        if self.__titre == "Guerrier":
            attacks = {pygame.K_a : ("Slam", 2, 1, 1, 5)}
        elif self.__titre == "Mage":
            attacks = {pygame.K_a : ("Fireball", 2, 1, 1, 5)}
        elif self.__titre == "Vampire":
            attacks = {pygame.K_a : ("Drain", 2, 1, 1, 5)}
        return attacks
    
class Attaque:
    def __init__(self, name, value, height, width, r, x, y):
        self.name = name
        self.value = value
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.range = r 

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE_H and 0 <= self.y + dy < GRID_SIZE_V:
            self.x += dx
            self.y += dy

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

    def __init__(self, x, y, health, attack_power, team, role, image_player = IMAGE, image_enemy = IMAGE, defense = 0, vitesse = 0):
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
        self.image_player = image_player
        self.image_enemy = image_enemy
        self.defense = defense
        self.vitesse = vitesse

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE_H and 0 <= self.y + dy < GRID_SIZE_V:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def get_attacks(self):
        print("mavais code")
        pass

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        if self.image_enemy != None or self.image_player!= None:
            image = self.image_player if self.team == 'player' else self.image_enemy
            if self.is_selected:
                pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                
            screen.blit(pygame.transform.scale(image , (CELL_SIZE, CELL_SIZE)),(self.x * CELL_SIZE, self.y * CELL_SIZE))

        else: 
            titre = self.role.get_titre()
            color = BLACK if self.team == 'enemy' else MAGE if titre == "Mage" else GUERRIER if titre == "Guerrier" else VAMPIRE
            if self.is_selected:
                pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                                self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        



class Vampire(Unit):

    def __init__(self, x, y, health, attack_power, team, role):
        super().__init__(x, y, health, attack_power, team, role, IMAGE_CROQUE_MINOU,IMAGE_MECHANT_MAGE)

    
    def get_attacks(self):
        attacks = {pygame.K_a : ("Drain", 2, 1, 1, 5), pygame.K_z: ("TBD", 2, 1, 1, 5), pygame.K_e : ("TBD", 2, 1, 1, 5)}
        return attacks


class Guerrier(Unit):

    def __init__(self, x, y, health, attack_power, team, role):
        super().__init__(x, y, health, attack_power, team, role, IMAGE, IMAGE_MECHANT_GUERRIER)
        

    def get_attacks(self):
        attacks = {pygame.K_a : ("Slam", 2, 1, 1, 5), pygame.K_z: ("TBD", 2, 1, 1, 5), pygame.K_e : ("TBD", 2, 1, 1, 5)}
        return attacks


class Mage(Unit):

    def __init__(self, x, y, health, attack_power, team, role):
        super().__init__(x, y, health, attack_power, team, role, IMAGE, IMAGE_MECHANT_VAMPIRE)
        
    def get_attacks(self):
        attacks = {pygame.K_a : ("Fireball", 2, 1, 1, 5), pygame.K_z: ("TBD", 2, 1, 1, 5), pygame.K_e : ("TBD", 2, 1, 1, 5)}
        return attacks
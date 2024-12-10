import pygame
import random
from image import *
from unit import *  

class Mage_player(Unit):
    def __init__(self, x, y, health, attack_power, image, defe, vit):
        super().__init__(x, y, health, attack_power, 'player', image, defe, vit)
        self.liste_attaque = ["Longue attaque", "Régène", "Bouclier"]


class Vampire_player(Unit):
    def __init__(self, x, y, health, attack_power, image, defe, vit):
        super().__init__(x, y, health, attack_power, 'player', image, defe, vit)
        self.liste_attaque = ["Vampiriser", "Furtif", "Brouiller"]


class Guerrier_player(Unit):
    def __init__(self, x, y, health, attack_power, image, defe, vit):
        super().__init__(x, y, health, attack_power, 'player', image, defe, vit)
        self.liste_attaque = ["Frappe", "Parer", "Attaque de groupe"]
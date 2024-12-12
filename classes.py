import pygame
import random
from image import *
from unit import *  

class Mage_player(Unit):
    def __init__(self, x, y, attack_power, image, defe, vit):
        super().__init__(x, y, attack_power, 'player', image, defe, vit)
        self.liste_attaque = ["Longue attaque", "Régène", "Bouclier"]

    def degat_subit():
        pass 
    

class Vampire_player(Unit):
    def __init__(self, x, y, attack_power, image, defe, vit):
        super().__init__(x, y, attack_power, 'player', image, defe, vit)
        self.liste_attaque = ["Vampiriser", "Furtif", "Brouiller"]


class Guerrier_player(Unit):
    def __init__(self, x, y, attack_power, image, defe, vit):
        super().__init__(x, y, attack_power, 'player', image, defe, vit)
        self.liste_attaque = ["Frappe", "Parer", "Attaque de groupe"]
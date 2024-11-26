# Map

import pygame
import random

from unit import *

# Fonction pour ajouter un mur
def couleur(x, y, largeur, hauteur, color):
    colors = []
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, largeur * CELL_SIZE, hauteur * CELL_SIZE)
    colors.append(rect)
    
    return colors

def mur():
    walls = []
    
    centre_x = GRID_SIZE_H//2
    centre_y = GRID_SIZE_V//2

    for i in range (GRID_SIZE_H) :
        for j in range (GRID_SIZE_V) :

             # Fonction pour ajouter un mur
            def ajouter_mur(x, y, largeur, hauteur):
                """Ajoute un mur de taille (largeur, hauteur) à la position (x, y)."""
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, largeur * CELL_SIZE, hauteur * CELL_SIZE)
                walls.append(rect)

            
            # Salle 1
            ajouter_mur(3, 0, 1, 3)  
            ajouter_mur(0, 5, 7, 1)
            ajouter_mur(6, 2, 1, 3)
            ajouter_mur(6, 2, 11, 1)  
            ajouter_mur(10, 6, 6, 1)
            ajouter_mur(10, 5, 1, 5)
            ajouter_mur(2, 9, 8, 1)

                        
            # Salle 2


            # Salle 3
            ajouter_mur(10, 18, 6, 1)
            ajouter_mur(10, 15, 1, 4)
            ajouter_mur(6, 13, 1, 9)
            ajouter_mur(7, 21, 10, 1)
            ajouter_mur(2, 15, 1, 9)

            # Condition pour dessiner la forme principale
            if (abs(i - centre_x) == 6 and abs(j - centre_y) <= 4) or \
               (abs(j - centre_y) == 6 and abs(i - centre_x) <= 4):
                rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                walls.append(rect)
            elif (i == centre_x and abs(j - centre_y) > 5) or \
                (j == centre_y and abs(i - centre_x) > 5):
                rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                walls.append(rect)
             
    return walls


    


"""
# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)           #base RVB
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class map:
    
    Classe pour représenter la map.
    

    def __init__(self) :

        def mur (x, y, largeur, hauteur, liste_murs):
            
            x: Position x du mur
            y: Position y du mur
            largeur: Largeur du mur
            hauteur: Hauteur du mur
            liste_murs: Liste des murs (modifiable)
               
            walls = []
            walls.append(pygame.Rect(120, 120, 60, 60))  # Mur au milieu
            walls.append(pygame.Rect(180, 180, 60, 60))  # Mur adjacent
            return walls
"""

        

       # def piège ():  --> augmenter les probas d'avoir un piège au fur et à mesure des niveaux



      #  def passages_secrets ():
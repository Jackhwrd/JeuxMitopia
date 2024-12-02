import pygame
import random
import numpy as np

from unit import *

def mur():
    walls = []
    
    centre_x = GRID_SIZE_H//2
    centre_y = GRID_SIZE_V//2

    # Création d'une grille de coordonnées
    x, y = np.meshgrid(np.arange(GRID_SIZE_H), np.arange(GRID_SIZE_V))

    # Créer les murs pour les différentes salles et zones
    wall_conditions = [
        # murs principaux
        ((x == centre_x) & (y < 6), (x == centre_x) & (y > centre_y+6), (x < centre_x - 6) & (y == centre_y), (x > centre_x + 6) & (y == centre_y)),

        # Salle 1 (coordonnées des murs)
        ((x == 3) & (y < 3), #bon
         (x <= 5) & (y == 5), #
         (x == 6) & (y >= 2) & (y <= 5), #bon
         (x >= 6) & (x <= centre_x - 4) & (y == 2), 
         (x >= 2) & (x <= 10) & (y == centre_y - 3), #bon
         (x == 10) & (y >= 5) & (y <= centre_y - 3), #bon
         (x >= 11) & (x <= 15) & (y == 6)),

        # Salle 3
        ( (x == 2) & (y >= 15), #bon
          (x == 6) & (y >= centre_y) & (y <= GRID_SIZE_V - 3), #bon
          (x >= 7) & (x <= centre_x - 3) & (y == GRID_SIZE_V - 3), #bon
          (x == 10) & (y >= centre_y + 3) & (y <= centre_y + 6), 
          (x >= 10) & (x <= 15) & (y == centre_y + 6)),    #bon
    ]

    for condition in wall_conditions:
        for cond in condition:
            walls.extend([pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE) 
                          for i, j in zip(x[cond], y[cond])])

    # Créer les murs principaux de la forme
    # Logique principale de forme
    main_shape_mask = (np.abs(x - centre_x) == 6) & (np.abs(y - centre_y) <= 4) | \
                      (np.abs(y - centre_y) == 6) & (np.abs(x - centre_x) <= 4)
    shape_coords = zip(x[main_shape_mask], y[main_shape_mask])
    walls.extend([pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE) for i, j in shape_coords])

    return walls

def generate_rooms(salles):
    """
    Divise la grille en cinq salles en utilisant NumPy.
    Retourne un tableau NumPy représentant les salles.
    """
    rooms = np.zeros((GRID_SIZE_H, GRID_SIZE_V), dtype=int)
    mid_x, mid_y = GRID_SIZE_H / 2, GRID_SIZE_V / 2

    for x in range(GRID_SIZE_H):
        for y in range(GRID_SIZE_V):
            if (x < mid_x and y < 7) or (x < 15 and y < mid_y):
                rooms[x, y] = salles[0].id  # Salle 1 (haut gauche)
            elif (x > mid_x and y < 7) or (x >= mid_x + 6 and y < mid_y):
                rooms[x, y] = salles[1].id  # Salle 2 (haut droit)
            elif (x < mid_x and y >= mid_y + 6) or (x < 15 and y > mid_y):
                rooms[x, y] = salles[2].id  # Salle 3 (bas gauche)
            elif (x > mid_x and y >= mid_y + 6) or (x >= mid_x + 6 and y > mid_y):
                rooms[x, y] = salles[3].id  # Salle 4 (bas droit)
            else:
                rooms[x, y] = salles[4].id  # Salle 5 (arène)

    return rooms

# détection des murs
def is_near_wall(grid_x, grid_y, walls):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # haut, bas, gauche, droite
        for dx, dy in directions:
            nx, ny = grid_x + dx, grid_y + dy
            # Créer un rectangle pour la cellule voisine
            neighbor_rect = pygame.Rect(nx * CELL_SIZE, ny * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if any(neighbor_rect.colliderect(wall) for wall in walls):
                return True
        return False
    
def get_cell_color(grid_x, grid_y, rooms, walls, salles):

    room_id = rooms[grid_x, grid_y]
    default_color = RED  
  
    # Trouver la salle correspondant à l'ID
    salle = next((s for s in salles if s.id == room_id), None)

    # Si aucune salle n'est trouvée, retourner une couleur par défaut
    if not salle:
        return default_color

    # Vérifier si la cellule est un mur
    cell_rect = pygame.Rect(grid_x * CELL_SIZE, grid_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    if any(cell_rect.colliderect(wall) for wall in walls):
        return BLACK  # Couleur des murs

    # Vérifier si la cellule est dans la salle 1 et si elle est proche d'un mur
    if room_id == 1:
        if is_near_wall(grid_x, grid_y, walls):
            return BROWN  # Marron (couleur Kaki) pour les cellules voisines des murs dans la salle 1

    #if room == 5:
    # Si la salle a un piège et est proche d'un mur
    if salle.piège and is_near_wall(grid_x, grid_y, walls):
        return BROWN  # Couleur pour une cellule piège  

    # Sinon, retourne la couleur de la salle
    return salle.couleur  

        

       # def piège ():  --> augmenter les probas d'avoir un piège au fur et à mesure des niveaux



      #  def passages_secrets ():
class salle :
        def __init__(self, id, couleur, piège=False, enemy=None, artefact=None):
            """def __init__(self, id, couleur, piège=False, ennemis=None, artefact=None):
        
        Initialise une salle avec ses caractéristiques.
        - id: identifiant de la salle (1, 2, 3, etc.)
        - couleur: couleur de la salle.
        - piège: booléen, s'il y a un piège dans la salle.
        - ennemis: liste ou nombre d'ennemis dans la salle.
        - artefact: description ou booléen pour savoir si un artefact est présent.
        """
            self.id = id
            self.couleur = couleur
            self.piège = piège
            self.enemy = enemy if enemy is not None else []
            self.artefact = artefact

        def afficher_infos(self):
            """Affiche les informations sur la salle."""
            print(f"Salle {self.id}:")
            print(f"  Piège: {'Oui' if self.piège else 'Non'}")
            print(f"  Ennemis: {self.enemy}")
            print(f"  Artefact: {self.artefact if self.artefact else 'Aucun'}")


cave = salle(1, KAKI, False, 3, None)
sellier = salle(2, BROWN, False, 3, None)
cuisines = salle(3, WHITE, False, 3, None)
ecuries = salle(4, YELLOW, False, 3, None)
arene = salle(5, RED, False, 3, None)

salles = [cave, sellier, cuisines, ecuries, arene]

for salle in salles:
    salle.afficher_infos()
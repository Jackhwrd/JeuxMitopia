import pygame
import random
import numpy as np

from unit import *

centre_x = GRID_SIZE_H//2
centre_y = GRID_SIZE_V//2

def mur():
    walls = []
    

    # Création d'une grille de coordonnées
    x, y = np.meshgrid(np.arange(GRID_SIZE_H), np.arange(GRID_SIZE_V))

    # Créer les murs pour les différentes salles et zones
    wall_conditions = [
        # murs des contours
        ((x == centre_x) & (y < 6), (x == centre_x) & (y > centre_y+6), 
         (x < centre_x - 6) & (y == centre_y), (x > centre_x + 6) & (y == centre_y),
         (x == 0) & (y >= 3) & (y <= GRID_SIZE_V-2),
         (x == GRID_SIZE_H-1) & (y >= 1) & (y <= GRID_SIZE_V),
         (x >= 3) & (x <= GRID_SIZE_H-3) & (y == 0),
         (x >= 3) & (x <= GRID_SIZE_H) & (y == GRID_SIZE_V-1)),

        # Salle 1 (coordonnées des murs)
        ((x == 3) & (y < 3), #bon
         (x <= 5) & (y == 5), #
         (x == 6) & (y >= 2) & (y <= 5), #bon
         (x >= 6) & (x <= centre_x - 4) & (y == 2), 
         (x >= 2) & (x <= 10) & (y == centre_y - 3), #bon
         (x == 10) & (y >= 5) & (y <= centre_y - 3), #bon
         (x >= 11) & (x <= 15) & (y == 6)),

        # Salle 2
        ( (x == GRID_SIZE_H - 5) & (y >= centre_y - 5) & (y <= centre_y), #bon
          (x == GRID_SIZE_H - 5) & (y <= 3), #bon
          (x == GRID_SIZE_H - 9) & (y <= 3),
          (x == GRID_SIZE_H - 13) & (y <= 3)),    #bon
        
        # Salle 3
        ( (x == 2) & (y >= 15), #bon
          (x == 6) & (y >= centre_y) & (y <= GRID_SIZE_V - 3), #bon
          (x >= 7) & (x <= centre_x - 3) & (y == GRID_SIZE_V - 3), #bon
          (x == 10) & (y >= centre_y + 3) & (y <= centre_y + 6), 
          (x >= 10) & (x <= 15) & (y == centre_y + 6)),    #bon

        # Salle 4
        ( (x == GRID_SIZE_H - 2) & (y >= centre_y) & (y < centre_y + 5),
          (x == GRID_SIZE_H - 2) & (y > centre_y + 6),
          (x == GRID_SIZE_H - 3) & (y >= centre_y) & (y < centre_y + 4),
          (x == GRID_SIZE_H - 3) & (y > centre_y + 7),
          (x == GRID_SIZE_H - 4) & (y == centre_y + 3),
          (x == GRID_SIZE_H - 4) & (y == centre_y + 8),
          (x >= GRID_SIZE_H - 7) & (x <= GRID_SIZE_H - 6) & (y == centre_y + 3),
          (x >= GRID_SIZE_H - 7) & (x <= GRID_SIZE_H - 6) & (y == centre_y + 8),
          (x >= GRID_SIZE_H - 11) & (x <= GRID_SIZE_H - 10) & (y == centre_y + 3),
          (x >= GRID_SIZE_H - 11) & (x <= GRID_SIZE_H - 10) & (y == centre_y + 8),
          (x >= centre_x + 4) & (x <= centre_x + 7) & (y == GRID_SIZE_V -2 )),    #bon
        
        # Salle 5
        ( (x >= centre_x - 1) & (x <= centre_x + 1) & (y == centre_y ), #bon
          (x == centre_x) & (y >= centre_y - 1) & (y <= centre_y + 1),
          (x == centre_x + 5) & (y == centre_y - 4),
          (x == centre_x + 5) & (y == centre_y + 4)),    #bon
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
    
    if room_id == 2:
        if is_near_wall(grid_x, grid_y, walls):
            return (120, 0, 60)
        
    if room_id == 3:
        if is_near_wall(grid_x, grid_y, walls):
            return (95, 158, 160)
    
    if room_id == 4:
        if is_near_wall(grid_x, grid_y, walls):
            return (128, 0, 0)
        
    if room_id == 5:
        if is_near_wall(grid_x, grid_y, walls):
            return (50, 8, 0)  # Marron (couleur Kaki) pour les cellules voisines des murs dans la salle 1


    #if room == 5:
    # Si la salle a un piège et est proche d'un mur
    if salle.piège and is_near_wall(grid_x, grid_y, walls):
        return BROWN  # Couleur pour une cellule piège  
    
    # Sinon, retourne la couleur de la salle
    return salle.couleur  

def teleport_unit(unit, target_pos, rooms, salles):
    """
    Téléporte une unité à une position cible et vérifie les conditions d'entrée.
    
    Args:
        unit (Unit): L'unité à téléporter.
        target_pos (tuple): Position cible (x, y) en cellules.
        rooms (np.ndarray): Tableau NumPy représentant les salles.
        salles (list): Liste des salles avec leurs conditions.
    """
    target_x, target_y = target_pos
    
    # Vérifier si les coordonnées sont valides dans la grille
    if not (0 <= target_x <= GRID_SIZE_H and 0 <= target_y <= GRID_SIZE_V):
        print("Position de téléportation invalide !")
        return
    
    # Identifier l'ID de la salle à la position cible
    room_id = rooms[target_x, target_y]
    salle = next((s for s in salles if s.id == room_id), None)
    
    if salle:
        # Vérifier les conditions d'entrée
        if salle.verifier_conditions(unit):
            # Téléporter l'unité
            unit.x, unit.y = target_pos
            print(f"L'unité {unit} a été téléportée à {target_pos}, dans la salle {salle.id}.")
        else:
            print(f"Accès refusé à la salle {salle.id}. Conditions non remplies.")
    else:
        # Si aucune salle n'est associée à la position, téléporter normalement
        unit.x, unit.y = target_pos
        print(f"L'unité {unit} a été téléportée à {target_pos}, hors d'une salle définie.")


       # def piège ():  --> augmenter les probas d'avoir un piège au fur et à mesure des niveaux



      #  def passages_secrets ():

class GameObject:
    def __init__(self, x, y, name, color):
        """
        Initialise un objet à une position spécifique.
        - x, y: Position de l'objet en cellules.
        - name: Nom de l'objet (ex: 'épée', 'potion').
        - color: Couleur utilisée pour dessiner l'objet.
        - effect_color: Couleur de l'effet (ex: vert pour le joueur)
        """
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        
    def draw(self, screen):
        """Dessine l'objet sur l'écran."""
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, self.color, rect)
    
    def __repr__(self):
        return f"GameObject({self.name}, {self.x}, {self.y})"

def generate_objects():
    """
    Crée une liste d'objets du jeu.
    """
    objets = [
        GameObject(4, 4, 'Clef', GREEN),  # Exemple : une épée
        GameObject(centre_x - 2, centre_y - 2, 'Badge', GREEN),  # badge
        GameObject((centre_x+8), (centre_y-5), 'Pierre de téléportation', GREEN)  #pass
    ]
    return objets

class salle:
    def __init__(self, id, couleur, piège=False, enemy=None, objet=None, conditions=None, x_min=0, x_max=10, y_min=0, y_max=10):
        """Initialise une salle avec ses caractéristiques.
        
        Paramètres :
            id (int): Identifiant de la salle (1, 2, 3, etc.).
            couleur (str): Couleur de la salle.
            piège (bool): Indique si la salle a un piège.
            enemy (list or int): Liste ou nombre d'ennemis dans la salle.
            objet (object): Un objet présent dans la salle (par exemple, une clé).
            conditions (dict): Conditions nécessaires pour accéder à la salle.
            x_min, x_max, y_min, y_max (int): Coordonnées de la salle (définit les limites de la salle).
        """
        self.id = id
        self.couleur = couleur
        self.piège = piège
        self.enemy = enemy if enemy is not None else []
        self.objet = objet
        self.conditions = conditions if conditions else {}
        self.ouverte = False # fermée par défaut
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
   
    def afficher_infos(self):
        print(f"Salle {self.id}:")
        print(f"  Piège: {'Oui' if self.piège else 'Non'}")
        print(f"  Ennemis: {self.enemy}")
        print(f"  Objet: {self.objet if self.objet else 'Aucun'}")
        print(f"  Conditions : {self.conditions}")
        print(f"  Coordonnées: x_min={self.x_min}, x_max={self.x_max}, y_min={self.y_min}, y_max={self.y_max}")
        print(f"  Ouverte : {'Oui' if self.ouverte else 'Non'}")

    def verifier_conditions(self, unit):
        if self.ouverte:
            print(f"Accès libre à la salle {self.id}.")
            return True  # La salle est déjà ouverte
        
        for condition, valeur in self.conditions.items():
            if condition == "Clef" and not any(obj.name == "Clef" for obj in unit.has_object):
                print("Condition manquante : clef requise.")
                return False
            if condition == "Badge" and not any(obj.name == "Badge" for obj in unit.has_object):
                print("Condition manquante : badge requis.")
                return False
            if condition == "Pierre de téléportation" and not any(obj.name == "Pierre de téléportation" for obj in unit.has_object):
                print("Condition manquante : Pierre de téléportation requise.")
                return False
            if condition == "niveau_min" and unit.niveau < valeur:
                print(f"Condition manquante : niveau {valeur} requis.")
                return False
        print(f"Accès à la salle {self.id} autorisé.")
        self.ouverte = True
        return True

class CaseRegeneration:
    def __init__(self, x, y, color):
        """Initialise la case de régénération à une position donnée"""
        self.x = x
        self.y = y
        self.color = color

    def appliquer_effet(self, unité, game):
        """
        Applique l'effet de régénération lorsqu'une unité se trouve sur cette case.
        unité : instance de l'unité qui se trouve sur la case
        game : instance du jeu contenant les unités
        """
        # Régénération pour l'unité qui se trouve sur la case
        regen = unité.health_max * 0.2  # Par exemple, régénérer 20% de la santé max
        unité.health = min(unité.health + regen, unité.health_max)  # Ne pas dépasser la santé max

        # Drain de vie des ennemis adjacents
        for enemy in game.enemy_units:
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 1:  # Pour les ennemis autour de la case
                degat = unité.puissance_attaque * unité.stat_attaque
                degat_final = enemy.degat_subit(unité, degat)
                enemy.update_health(degat_final)
                unité.health = min(unité.health + degat_final / 2, unité.health_max)
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
                break  # On affecte un seul ennemi à la fois
        """
        # (Optionnel) Donner de la santé à une unité alliée proche
        for ami in game.player_units:
            distance = abs(self.x - ami.x) + abs(self.y - ami.y)
            if 1 <= distance <= 1 and ami != unité:
                soin = unité.health * 0.1  # Donne 10% de la santé actuelle de l'unité active
                ami.health = min(ami.health + soin, ami.health_max)
                unité.health -= soin
                """
    def draw(self, screen):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, self.color, rect)
    
def generate_cases():
    
    cases_regeneration = [
        CaseRegeneration (centre_x + 2, GRID_SIZE_V - 3, LIGHT_YELLOW),
        CaseRegeneration (centre_x + 2, GRID_SIZE_V - 4, LIGHT_YELLOW)
        ]
    return cases_regeneration

class Trap:
    def __init__(self, x, y, color, trap_type, damage=0, effect=None):
        """Initialise la case de régénération à une position donnée"""
        self.x = x
        self.y = y
        self.color = color
        self.trap_type = trap_type
        self.damage = damage
        self.effect = effect
        self.is_active = True  # Le piège peut être désactivé après activation
        

    def trigger(self, unit):
        """
        Active le piège lorsqu'une unité marche dessus.
        :param unit: L'unité affectée par le piège.
        """
        if not self.is_active:
            print(f"Le piège ({self.trap_type}) à ({self.x}, {self.y}) est déjà désactivé.")
            return False
        else :
            if self.trap_type == "poison":  # Exemple, si le piège est un spike, il bloque le mouvement
                print(f"Le piège ({self.trap_type}) s'active sur {unit}.")
                unit.update_health(self.damage)  # Applique des dégâts à l'unité
                print(f'Damage {unit} = {unit.health - self.damage}')
                self.is_active = False  # Désactive le piège après activation
            if self.trap_type == "spikes":  # Exemple, si le piège est un spike, il bloque le mouvement
                print(f"Le piège ({self.trap_type}) s'active sur {unit}.")
                unit.update_health(self.damage)  # Applique des dégâts à l'unité
                print(f'Damage {unit} = {unit.health - self.damage}')
                self.is_active = False  # Désactive le piège après activation
        return True
    
    def reactivate(self):
        """Réactive le piège."""
        self.is_active = True
        self.block_movement = False  # Réactive également la possibilité de se déplacer sur la case
        print(f"Le piège ({self.trap_type}) à ({self.x}, {self.y}) est réactivé.")

    def draw(self, screen):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, self.color, rect)
    
def generate_traps():
    
    traps = [
        Trap (2, 3, KAKI, "spikes", damage=10),
        Trap (GRID_SIZE_H - 3, GRID_SIZE_V - 5, YELLOW, "poison", damage=5)
        ]
    for trap in traps:
        print(f"Piège généré : {trap.trap_type} à ({trap.x}, {trap.y})")  # Debug
    return traps

# Création d'un objet GameObject
clef = GameObject(4, 4, 'Clef', GREEN)
badge = GameObject(centre_x, centre_y, 'Badge', GREEN)
pierre = GameObject((centre_x+8), (centre_y-5), 'Pierre de téléportation', GREEN)  #pass

# Création des salles
cave = salle(1, KAKI, False, 3, objet=clef)
sellier = salle(2, (0, 255, 0), False, 3, objet=pierre, conditions={"Badge": True})
cuisines = salle(3, WHITE, False, 3, conditions={"Pierre de téléportation": True})
ecuries = salle(4, YELLOW, False, 3)
arene = salle(5, RED, False, 3, objet=badge, conditions={"Clef": True})

salles = [cave, sellier, cuisines, ecuries, arene]
"""
# Création des cases de régénération
case1 = CaseRegeneration (centre_x + 2, GRID_SIZE_V - 3, LIGHT_YELLOW)
case2 = CaseRegeneration (centre_x + 2, GRID_SIZE_V - 2, LIGHT_YELLOW)

cases_regeneration = [case1, case2]

# Création des pièges
trap1 = Trap (2, 6, KAKI, "spikes", damage=10)
trap2 = Trap (GRID_SIZE_H - 3, GRID_SIZE_V - 5, YELLOW, "poison", damage=5, effect="poison")

traps = [trap1, trap2]
"""
for salle in salles:
    salle.afficher_infos()

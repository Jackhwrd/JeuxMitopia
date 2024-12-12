import pygame
import random
from image import *


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

    def __init__(self, x, y, attack_power, team,image,defe,attaque,vit,niveau = 1):
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
        self.health = 100
        self.puissance_attaque = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.character_image = image
        self.stat_defense = defe
        self.stat_attaque = attaque
        self.vitess = vit
        self.has_object = []
        self.niveau = niveau  # Niveau du joueur
        self.max_health = 100
        self.en_vie = True 
        
        

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
            
    def augmenter_niveau(self):
        self.niveau += 1
        print(f"Votre niveau a augmenté : {self.niveau}")

    def collect(self, obj):
        # Si l'objet n'est pas déjà dans la liste, on l'ajoute
        if obj.name not in [o.name for o in self.has_object]:
            self.has_object.append(obj)
            print(f"Vous avez ramassé : {obj.name}!")
            
    def update_health(self,degat) : 
        if self.health - degat > degat : #Le joueur à assez de vie pour subir le degat
            self.health -= degat 
        else:
            #si le joueur n'a plus de point de vie il doit mourir 
            self.en_vie = False

    def update_health_bar(self, surface):
        
        # Position et dimensions pour que ce soit juste en dessous du perso
        bar_x = self.x * CELL_SIZE + 5  
        bar_y = self.y * CELL_SIZE + CELL_SIZE 
        
        # Largeur de la barre de vie 
        bar_width = CELL_SIZE  
        bar_height = 5  
        
        # Dessiner la barre d'arrière-plan
        pygame.draw.rect(surface, background_color, [bar_x, bar_y, bar_width, bar_height])
        
        # Dessiner la barre de vie (proportionnelle à la santé restante)
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(surface, health_color, [bar_x, bar_y, health_width, bar_height])

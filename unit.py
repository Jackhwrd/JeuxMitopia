import pygame
import random
from image import *


class Unit:

    def __init__(self, x, y, health, attack_power, team,image,defe,vit,niveau = 1):
        
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.niveau = niveau  # Niveau du joueur
        self.is_selected = False
        self.character_image = image
        self.defense = defe
        self.vitess = vit
        self.has_object = []
        self.niveau = niveau  # Niveau du joueur

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
                    
    def augmenter_niveau(self):
        self.niveau += 1
        print(f"Votre niveau a augmenté : {self.niveau}")

    def collect(self, obj):
        # Si l'objet n'est pas déjà dans la liste, on l'ajoute
        if obj.name not in [o.name for o in self.has_object]:
            self.has_object.append(obj)
            print(f"Vous avez ramassé : {obj.name}!")
            
    def health(self,degat) : 

        pass 

    def update_health_bar():
        pass 

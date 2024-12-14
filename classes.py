import pygame
import random
from image import *
from unit import *  
from game import *

class Mage_player(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 8, 'player', image_croque_minou, 0.8,1,1)
        self.liste_attaque = ["Longue attaque", "Régène", "Bouclier"]
        self.type = "Mage"

    def Longue_attaque(self, game):
        """Attaque à distance sur les ennemis qui sont dans une zone d'attaque de 4 à 6 carreaux avec un peu moins de puissance"""
        
        for enemy in game.enemy_units:
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 4 <= distance <= 6:  # Entre 4 et 6 cases de distance

                degat = self.puissance_attaque * self.stat_attaque*0.85
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)

    def Regene(self,game):
        """attaque qui permet de se regenerer avec la vie d'un ennemie ou de donner de la vie à un joueur"""

        for enemy in game.enemy_units: #pour prendre la vie d'un montre 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 1:  # pour les 8 cases autour du joueur 

                degat = self.puissance_attaque * self.stat_attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                self.health += degat_final / 2 #pour recupere la moitier de la vie prise 
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
                break 

        for ami in game.player_units:

            vie = self.health * 0.15 # pour prendre 15% de la vie restante lors du tour 
            distance = abs(self.x - ami.x) + abs(self.y - ami.y)
            if 1 <= distance <= 1 :  #pour les 8 cases autour du joueur 

                
                ami.health += vie 
                self.health -= vie 

    def Bouclier(self,game): 
        """attaque qui permet d'augmenter sa stat de defense ainsi que ces amie dans un rayon de 1 bloque mais qui baisse un peu son attaque """
        self.stat_defense += 0.1
        if self.stat_attaque - 0.05 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
            self.stat_attaque = 0.1
        else : 
            self.stat_attaque -= 0.05

        for ami in game.player_unit:
            distance = abs(self.x - ami.x) + abs(self.y - ami.y)
            if 1 <= distance <= 1:  # pour les 8 cases autour du joueur 

                ami.stat_defense += 0.1
        

    def degat_subit(self,monstre,degat):
        """Fonction qui permet de calculer le dommage final en suivant du type de l'attaquant """
        if monstre.type == "Mage": 
            degat_final = degat 
        elif monstre.type == "Vampire" : 
            degat_final = degat*2
        elif monstre.type == "Guerrier": 
            degat_final = degat / 2
        
        return degat_final-(degat*self.stat_defense)
    
    def attaque(self,attaque_choisie,game):
        
        if attaque_choisie == "Longue attaque":

            self.Longue_attaque(game)
        elif attaque_choisie == "Régène" : 
            self.Regene(game)
        elif attaque_choisie == "Bouclier" : 
            self.Bouclier(game)

class Vampire_player(Unit):

    
    def __init__(self, x, y):
        super().__init__(x, y, 10, 'player', image_vampire, 0.5,1, 1)
        self.liste_attaque = ["Vampiriser", "Furtif", "Brouiller"]
        self.type = "Vampire"

    def Vampiriser(self,game) :
        """Prend de la vie de tout les monstres dans un rayon de 2 block au alentour"""
        for enemy in game.enemy_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 2:  # pour les 17 cases autour du joueur 

                degat = self.puissance_attaque * self.stat_attaque * 0.85 # pour dimunier la puissance de l'attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                self.health += degat_final / 2  #pour recupere la moitier de la vie prise 
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
    
    def Furtif(self,game) : 
        "Tape un adversaire qui se trouve dans un rayon de 4 Block "
        for enemy in game.enemy_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 4:  

                degat = self.puissance_attaque * self.stat_attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
            break 

    def Brouiller(self,game) : 
        """ Fait baisser la defense des adversaire dans un rayon de 2 block autour d'elle, et recuper cette stat en attaque, sa defense baisse légérement"""
        for enemy in game.enemy_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 2:   
                
                if self.stat_defense - 0.05 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
                    self.stat_defense = 0.1
                else : 
                     self.stat_defense -= 0.05

                if enemy.stat_defense - 0.1 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
                    enemy.stat_defense = 0.1
                else : 
                     enemy.stat_defense -= 0.1  
                
                self.stat_attaque += 0.1

    def attaque(self,attaque_choisie,game):
        
        if attaque_choisie == "Vampiriser":
            self.Vampiriser(game)
        elif attaque_choisie == "Furtif" : 
            self.Furtif(game)
        elif attaque_choisie == "Brouiller" : 
            self.Brouiller(game)

    def degat_subit(self,monstre,degat):
        """Fonction qui permet de calculer le dommage final en suivant du type de l'attaquant """

        if monstre.type == "Mage": 
            degat_final = degat / 2
        elif monstre.type == "Vampire" : 
            degat_final = degat
        elif monstre.type == "Guerrier": 
            degat_final = degat * 2
            
        return degat_final-(degat*self.stat_defense)

class Guerrier_player(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 12, 'player', image_guts, 0.3,1, 1)
        self.liste_attaque = ["Frappe", "Intimidation", "Attaque de groupe"]
        self.type = "Guerrier"

    def Frappe(self,game): 
        """frappe un enemie dans une zone de 1 carreaux"""
        for enemy in game.enemy_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 1:  

                degat = self.puissance_attaque * self.stat_attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)

            break 

    def Intimidation(self,game) : 
        """Fait peur au enemy au alentour, fait baisser leur stat d'attaque, perd un peu de defense, monte également son attaque"""
        for enemy in game.enemy_units:
            if self.stat_defense - 0.05 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
                    self.stat_defense = 0.1
            else : 
                     self.stat_defense -= 0.05

            if enemy.stat_attaque - 0.1 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
                    enemy.stat_attaque = 0.1
            else : 
                enemy.stat_attaque -= 0.1  
                
                self.stat_attaque += 0.1



    def Attaque_de_groupe(self,game) : 
        "frappe tout les enemie dans un rayon de 2 block mais avec un peu moins de force"

        for enemy in game.enemy_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 2:  

                degat = self.puissance_attaque * self.stat_attaque * 0.85
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
                    
    def attaque(self,attaque_choisie,game):
        
        if attaque_choisie == "Frappe":
            self.Frappe(game)
        elif attaque_choisie == "Intimidation" : 
            self.Intimidation(game)
        elif attaque_choisie == "Attaque de groupe" : 
            self.Attaque_de_groupe(game)
        

    def degat_subit(self,monstre,degat):
        """Fonction qui permet de calculer le dommage final en suivant du type de l'attaquant ainsi que de la statistique de defense"""

        if monstre.type == "Mage": 
            degat_final = degat * 2
        elif monstre.type == "Vampire" : 
            degat_final = degat/2
        elif monstre.type == "Guerrier": 
            degat_final = degat 
            
        return degat_final-(degat_final*self.defense)
    

class Vampire_enemy(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 'enemy', image_mechant_vampire,0.5,1,1)
        self.liste_attaque = ["Vampiriser", "Furtif", "Brouiller"]
        self.type = "Vampire"

    def Vampiriser(self,game) :
        """Prend de la vie de tout les monstres dans un rayon de 2 block au alentour"""
        for enemy in game.player_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 2:  # pour les 17 cases autour du joueur 

                degat = self.puissance_attaque * self.stat_attaque * 0.85 # pour dimunier la puissance de l'attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                self.health += degat_final / 2  #pour recupere la moitier de la vie prise 
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
    
    def Furtif(self,game) : 
        "Tape un adversaire qui se trouve dans un rayon de 4 Block "
        for enemy in game.player_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 4:  

                degat = self.puissance_attaque * self.stat_attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
            break 

    def Brouiller(self,game) : 
        """ Fait baisser la defense des adversaire dans un rayon de 2 block autour d'elle, et recuper cette stat en attaque, sa defense baisse légérement"""
        for enemy in game.player_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 2:   
                if self.stat_defense - 0.05 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
                    self.stat_defense = 0.1
                else : 
                     self.stat_defense -= 0.05

                if enemy.stat_defense - 0.1 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
                    enemy.stat_defense = 0.1
                else : 
                     enemy.stat_defense -= 0.1  
                
                self.stat_attaque += 0.1
                

    def attaque(self,attaque_choisie,game):
        
        if attaque_choisie == "Vampiriser":
            self.Vampiriser(game)
        elif attaque_choisie == "Furtif" : 
            self.Furtif(game)
        elif attaque_choisie == "Brouiller" : 
            self.Brouiller(game)

    def degat_subit(self,monstre,degat):
        """Fonction qui permet de calculer le dommage final en suivant du type de l'attaquant """

        if monstre.type == "Mage": 
            degat_final = degat / 2
        elif monstre.type == "Vampire" : 
            degat_final = degat
        elif monstre.type == "Guerrier": 
            degat_final = degat * 2
            
        return degat_final-(degat*self.stat_defense)
    

class Guerrier_enemy(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 'enemy', image_mechant_vampire,0.5,1,1)
        self.liste_attaque = ["Vampiriser", "Furtif", "Brouiller"]
        self.type = "Vampire"

    def Frappe(self,game): 
        """frappe un enemie dans une zone de 1 carreaux"""
        for enemy in game.player_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 1:  

                degat = self.puissance_attaque * self.stat_attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)

            break 

    def Intimidation(self,game) : 
        """Fait peur au enemy au alentour, fait baisser leur stat d'attaque, perd un peu de defense, monte également son attaque"""
        for enemy in game.player_units:
            if self.stat_defense - 0.05 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
                    self.stat_defense = 0.1
            else : 
                     self.stat_defense -= 0.05

            if enemy.stat_attaque - 0.1 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
                    enemy.stat_attaque = 0.1
            else : 
                enemy.stat_attaque -= 0.1  
                
                self.stat_attaque += 0.1



    def Attaque_de_groupe(self,game) : 
        "frappe tout les enemie dans un rayon de 2 block mais avec un peu moins de force"

        for enemy in game.player_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 2:  

                degat = self.puissance_attaque * self.stat_attaque * 0.85
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
                    
    def attaque(self,attaque_choisie,game):
        
        if attaque_choisie == "Frappe":
            self.Frappe(game)
        elif attaque_choisie == "Intimidation" : 
            self.Intimidation(game)
        elif attaque_choisie == "Attaque de groupe" : 
            self.Attaque_de_groupe(game)
        

    def degat_subit(self,monstre,degat):
        """Fonction qui permet de calculer le dommage final en suivant du type de l'attaquant ainsi que de la statistique de defense"""

        if monstre.type == "Mage": 
            degat_final = degat * 2
        elif monstre.type == "Vampire" : 
            degat_final = degat/2
        elif monstre.type == "Guerrier": 
            degat_final = degat 
            
        return degat_final-(degat_final*self.defense)
    
class Mage_enemy(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 'enemy', image_mechant_mage,0.5,1,1)
        self.liste_attaque = ["Vampiriser", "Furtif", "Brouiller"]
        self.type = "Vampire"

    def degat_subit(self,monstre,degat):
        """Fonction qui permet de calculer le dommage final en suivant du type de l'attaquant """
        if monstre.type == "Mage": 
            degat_final = degat 
        elif monstre.type == "Vampire" : 
            degat_final = degat*2
        elif monstre.type == "Guerrier": 
            degat_final = degat / 2
        
        return degat_final-(degat*self.stat_defense)
    
    def Longue_attaque(self, game):
        """Attaque à distance sur les ennemis qui sont dans une zone d'attaque de 4 à 6 carreaux."""
        
        for enemy in game.enemy_units:
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 4 <= distance <= 6:  # Entre 4 et 6 cases de distance

                degat = self.puissance_attaque * self.stat_attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
                    
                

    def Regene(self,game):
        """attaque qui permet de se regenerer avec la vie d'un ennemie ou de donner de la vie à un joueur"""

        for enemy in game.player_units: #pour prendre la vie d'un montre 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 1 <= distance <= 1:  # pour les 8 cases autour du joueur 

                degat = self.puissance_attaque * self.stat_attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                self.health += degat_final / 2 #pour recupere la moitier de la vie prise 
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)

        for ami in game.enemy_unit:

            vie = self.health * 0.15 # pour prendre 15% de la vie restante lors du tour 
            distance = abs(self.x - ami.x) + abs(self.y - ami.y)
            if 1 <= distance <= 1 :  #pour les 8 cases autour du joueur 

                
                ami.health += vie 
                self.health -= vie 

    def Bouclier(self,game): 
        """attaque qui permet d'augmenter sa stat de defense ainsi que ces amie dans un rayon de 1 bloque mais qui baisse son attaque """
        self.stat_defense += 0.1
        if self.stat_attaque - 0.05 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
            self.stat_attaque = 0.1
        else : 
            self.stat_attaque -= 0.05

        for ami in game.enemy_unit:
            distance = abs(self.x - ami.x) + abs(self.y - ami.y)
            if 1 <= distance <= 1:  # pour les 8 cases autour du joueur 

                ami.stat_defense += 0.1

    def attaque(self,attaque_choisie,game):
        
        if attaque_choisie == "Longue attaque":

            self.Longue_attaque(game)
        elif attaque_choisie == "Régène" : 
            self.Regene(game)
        elif attaque_choisie == "Bouclier" : 
            self.Bouclier(game)

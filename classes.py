import pygame
import random
from image import *
from unit import *  
from game import *

class Mage_player(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 14, 'player', image_croque_minou, 0.8,1,6)
        self.liste_attaque = ["Longue attaque", "Régène", "Bouclier"]
        self.type = "Mage"

    def Longue_attaque(self, game, attaque):
        """Attaque à distance sur les ennemis qui sont dans une zone d'attaque de 4 à 6 carreaux avec un peu moins de puissance"""
        x, y = attaque.x, attaque.y
        if game.is_occupied_by_enemy(x, y):
            enemy = game.unit_at_position(x, y)
            degat = self.puissance_attaque * self.stat_attaque*0.85
            degat_final = enemy.degat_subit(self, degat)
            enemy.update_health(degat_final)
            print(f"Enemie {enemy.type} est frappée et reçoit {degat_final} points de dégats")
            if not enemy.en_vie:
                game.enemy_units.remove(enemy)
                print(f"Enemie {enemy.type} est mort!")
        else:
            print("Il faut selectionner un enemie!")
            return attaque
        
        return None

    def Regene(self,game):
        """attaque qui permet de se regenerer avec la vie d'un ennemie ou de donner de la vie à un joueur"""
        print("dans attaque regene")
        for enemy in game.enemy_units: #pour prendre la vie d'un monstre 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 0 <= distance < 2:  # pour les 8 cases autour du joueur 

                degat = self.puissance_attaque * self.stat_attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                if self.health + degat_final / 2 <= self.max_health :
                    self.health += degat_final / 2 #pour recupere la moitier de la vie prise 
                else :
                    self.health = self.max_health
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
                break 

        for ami in game.player_units:

            vie = self.health * 0.15 # pour prendre 15% de la vie restante lors du tour 
            distance = abs(self.x - ami.x) + abs(self.y - ami.y)
            if 0 <= distance < 2 :  #pour les 8 cases autour du joueur 

                if ami.health + vie / 2 <= ami.max_health :
                    ami.health += vie / 2 #pour recupere la moitier de la vie prise 
                else :
                    ami.health = self.max_health
                
                self.health -= vie 
    

    def Bouclier(self,game): 
        """attaque qui permet d'augmenter sa stat de defense ainsi que ces amie dans un rayon de 1 bloque mais qui baisse un peu son attaque """
        self.stat_defense += 0.1
        if self.stat_attaque - 0.05 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
            self.stat_attaque = 0.1
        else : 
            self.stat_attaque -= 0.05

        for ami in game.player_units:
            distance = abs(self.x - ami.x) + abs(self.y - ami.y)
            if 0 <= distance <= 2:  # pour les 8 cases autour du joueur 

                ami.stat_defense += 0.1
        

    def degat_subit(self,monstre,degat):
        """Fonction qui permet de calculer le dommage final en suivant du type de l'attaquant """
        if monstre.type == "Mage": 
            degat_final = degat 
        elif monstre.type == "Vampire" : 
            degat_final = degat*2
        elif monstre.type == "Guerrier": 
            degat_final = degat / 2
        else : 
            degat_final = degat
        
        return degat_final-(degat*self.stat_defense)
    
#    def attaque(self,attaque_choisie,game):
#        
#        if attaque_choisie == "Longue attaque":
#            self.Longue_attaque(game)
#        elif attaque_choisie == "Régène" : 
#            self.Regene(game)
#        elif attaque_choisie == "Bouclier" : 
#            self.Bouclier(game)

    def vise_attaque(self,attaque_choisie,game):
        
        if attaque_choisie == "Longue attaque":
            return Attaque("Longue attaque", 15, self.x, self.y, image_viseur, (0,0))
        elif attaque_choisie == "Régène" : 
            self.Regene(game)
        elif attaque_choisie == "Bouclier" : 
            self.Bouclier(game)

    def execute_attaque(self,game,attaque=None):
        
        if attaque.name == "Longue attaque":
            return self.Longue_attaque(game,attaque)

class Vampire_player(Unit):

    
    def __init__(self, x, y):
        super().__init__(x, y, 20, 'player', image_vampire, 0.5,1, 9)
        self.liste_attaque = ["Vampiriser", "Furtif", "Brouiller"]
        self.type = "Vampire"

    def Vampiriser(self,game) :
        """Prend de la vie de tout les monstres dans un rayon de 2 block au alentour"""
        n_enemy = 0
        hp_gagné = 0
        for enemy in game.enemy_units: 
            #distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            #if 0 <= distance <3:  # pour les 17 cases autour du joueur 
            if abs(self.x - enemy.x) < 3 and abs(self.y - enemy.y) < 3:
                degat = self.puissance_attaque * self.stat_attaque * 0.85 # pour dimunier la puissance de l'attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                if self.health + degat_final / 2 <= self.max_health :
                    self.health += degat_final / 2 #pour recupere la moitier de la vie prise 
                else :
                    self.health = self.max_health
                 
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
                    print(f"enemy {enemy.type} est mort!")
                
                n_enemy += 1
                hp_gagné += degat_final / 2
        
        if n_enemy:
            print(f"Batorie vampirise {n_enemy} et regagne {hp_gagné} points de vie")
        else:
            print(f"Batorie a completement raté son attaque???")

        return None
    
    def Furtif(self,game) : 
        "Tape un adversaire qui se trouve dans un rayon de 4 Block "
        for enemy in game.enemy_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 0 <= distance <= 4:  

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
            if 0 <= distance < 3:   
                
                if self.stat_defense - 0.05 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
                    self.stat_defense = 0.1
                else : 
                     self.stat_defense -= 0.05

                if enemy.stat_defense - 0.1 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
                    enemy.stat_defense = 0.1
                else : 
                     enemy.stat_defense -= 0.1  
                
                self.stat_attaque += 0.1

# def attaque(self, attaque_choisie, game):
#     if attaque_choisie == "Vampiriser":
#         self.Vampiriser(game)
#     elif attaque_choisie == "Furtif":
#         self.Furtif(game)
#     elif attaque_choisie == "Brouiller":
#         self.Brouiller(game)


    def vise_attaque(self,attaque_choisie,game):
        if attaque_choisie == "Vampiriser":
            return Attaque("Vampiriser", 0, self.x, self.y, zone_vampiriser, (-2,-2))
        elif attaque_choisie == "Furtif" : 
            self.Furtif(game)
        elif attaque_choisie == "Brouiller" : 
            self.Brouiller(game)
    
    def execute_attaque(self,game,attaque=None):
        
        if attaque.name == "Vampiriser":
            return self.Vampiriser(game)
        

    def degat_subit(self,monstre,degat):
        """Fonction qui permet de calculer le dommage final en suivant du type de l'attaquant """

        if monstre.type == "Mage": 
            degat_final = degat / 2
        elif monstre.type == "Vampire" : 
            degat_final = degat
        elif monstre.type == "Guerrier": 
            degat_final = degat * 2
        else :
            degat_final = degat
            
        return degat_final-(degat*self.stat_defense)

class Guerrier_player(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 25, 'player', image_guts, 0.3,1, 12)
        self.liste_attaque = ["Lancer", "Intimidation", "Frappe"]
        self.type = "Guerrier"

    def Frappe(self,game): 
        """frappe un enemie dans une zone de 1 carreaux"""
        for enemy in game.enemy_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 0 <= distance <= 2:  

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



    def Lancer(self,game,attaque): 
        "Lance un joueur ou un enemy ine certaine distance"
        if game.is_wall(attaque.x,attaque.y):
            print("Destination impossible")
            return attaque
        for unit in game.enemy_units + game.player_units:
            if unit.is_selected:
                unit.x, unit.y = attaque.x, attaque.y
                if unit.team == "enemy":
                    degat = self.puissance_attaque * self.stat_attaque * 2 if is_near_wall(attaque.x, attaque.y) else self.puissance_attaque * self.stat_attaque * 0.85 
                    degat_final = unit.degat_subit(self, degat)
                    unit.update_health(degat_final)
                print(f"l'alliée {unit.type} est propulsé vers case sélectionné") if unit.team == "player" else print(f"l'enemie {unit.type} percute le mur et reçoit {degat_final}!") if is_near_wall(attaque.x, attaque.y) else print(f"l'enemie s'envole et reçoit {degat_final}")
                if not unit.en_vie:
                        game.enemy_units.remove(unit)
                        print(f"l'enemie {unit.type} est mort!")
        return None



    def __Grab(self,game,attaque):
        x, y = attaque.x, attaque.y
        if game.is_occupied_by_unit(x, y):
            unit = game.unit_at_position(x, y)
            unit.is_selected = True
            print(f"vous attrapez {unit.team} {unit.type} et vous vous préparez au lancé")
            return Attaque("Lancer", 8, self.x, self.y, image_viseur, (0,0), True)
        else:
            print("Il vaut attraper un unit")
            return attaque



    

                    
# def attaque(self, attaque_choisie, game):

#     if attaque_choisie == "Frappe":
#         self.Frappe(game)
#     elif attaque_choisie == "Intimidation":
#         self.Intimidation(game)
#     elif attaque_choisie == "Attaque de groupe":
#         self.Attaque_de_groupe(game)

    def vise_attaque(self,attaque_choisie,game):
        
        if attaque_choisie == "Frappe":
            self.Frappe(game)
        elif attaque_choisie == "Intimidation" : 
            self.Intimidation(game)
        elif attaque_choisie == "Lancer" : 
            return Attaque("Grab", 1, self.x, self.y, image_selectionner_allié, (0,0))

    def execute_attaque(self,game,attaque=None):
        
        if attaque.name == "Grab":
            return self.__Grab(game,attaque)
        if attaque.name == "Lancer":
            return self.Lancer(game, attaque)
        

    def degat_subit(self,monstre,degat):
        """Fonction qui permet de calculer le dommage final en suivant du type de l'attaquant ainsi que de la statistique de defense"""

        if monstre.type == "Mage": 
            degat_final = degat * 2
        elif monstre.type == "Vampire" : 
            degat_final = degat/2
        elif monstre.type == "Guerrier": 
            degat_final = degat 
        else : 
            degat_final = degat
            
        return degat_final-(degat_final*self.stat_defense)
    

class Vampire_enemy(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 14, 'enemy', image_mechant_vampire,0.5,1,5)
        self.liste_attaque = ["Vampiriser", "Furtif", "Brouiller"]
        self.type = "Vampire"

    def Vampiriser(self,game) :
        """Prend de la vie de tout les monstres dans un rayon de 2 block au alentour"""
        for enemy in game.player_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 0 <= distance <= 2:  # pour les 17 cases autour du joueur 

                degat = self.puissance_attaque * self.stat_attaque * 0.85 # pour dimunier la puissance de l'attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                if self.health + degat_final / 2 <= self.max_health :
                    self.health += degat_final / 2 #pour recupere la moitier de la vie prise 
                else :
                    self.health = self.max_health
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
    
    def Furtif(self,game) : 
        "Tape un adversaire qui se trouve dans un rayon de 4 Block "
        for enemy in game.player_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 0 <= distance <= 4:  

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
            if 0 <= distance <= 2:   
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
        super().__init__(x, y, 17, 'enemy', image_mechant_guerier ,0.5,1,7)
        self.liste_attaque = ["Frappe", "Intimidation", "Attaque de groupe"]
        self.type = "Guerrier"

    def Frappe(self,game): 
        """frappe un enemie dans une zone de 1 carreaux"""
        for enemy in game.player_units: 
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 0 <= distance <= 2:  

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
            if 0 <= distance < 3:  

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
            
        return degat_final-(degat*self.stat_defense)
    
class Mage_enemy(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 12, 'enemy', image_mechant_mage,0.5,1,3)
        self.liste_attaque = ["Longue attaque", "Régène", "Bouclier"]
        self.type = "Mage"

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
        
        for enemy in game.player_units:
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
            if 0 <= distance <= 2:  # pour les 8 cases autour du joueur 

                degat = self.puissance_attaque * self.stat_attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                if self.health + degat_final / 2 <= self.max_health :
                    self.health += degat_final / 2 #pour recupere la moitier de la vie prise 
                else :
                    self.health = self.max_health
                
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)

        for ami in game.enemy_units:

            vie = self.health * 0.15 # pour prendre 15% de la vie restante lors du tour 
            distance = abs(self.x - ami.x) + abs(self.y - ami.y)
            if 0<= distance <= 2 :  #pour les 8 cases autour du joueur 

                if ami.health + vie / 2 <= ami.max_health :
                    ami.health += vie / 2 #pour recupere la moitier de la vie prise 
                else :
                    ami.health = self.max_health
                
                self.health -= vie 

    def Bouclier(self,game): 
        """attaque qui permet d'augmenter sa stat de defense ainsi que ces amie dans un rayon de 1 bloque mais qui baisse son attaque """
        self.stat_defense += 0.1
        if self.stat_attaque - 0.05 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
            self.stat_attaque = 0.1
        else : 
            self.stat_attaque -= 0.05

        for ami in game.enemy_units:
            distance = abs(self.x - ami.x) + abs(self.y - ami.y)
            if 0 <= distance <= 2:  # pour les 8 cases autour du joueur 

                ami.stat_defense += 0.1

    def attaque(self,attaque_choisie,game):
        
        if attaque_choisie == "Longue attaque":

            self.Longue_attaque(game)
        elif attaque_choisie == "Régène" : 
            self.Regene(game)
        elif attaque_choisie == "Bouclier" : 
            self.Bouclier(game)

class Status_enemy(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 'enemy', image_status,0.8,1,2)
        self.liste_attaque = ["Peur", "Onde de choc ", "Touche loin"]
        self.type = "Status"


    def Peur(self,game) : 
        for enemy in game.player_units:
            """Fait peur au joueur se trouvant dans un rayon de 3 block au alentour, fait baisser leur attaque """

            if enemy.stat_attaque - 0.1 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
                    enemy.stat_attaque = 0.1
            else : 
                enemy.stat_attaque -= 0.1  

    def Onde_de_choc(self,game) : 
        for enemy in game.player_units:
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 0 <= distance <= 2:  

                degat = self.puissance_attaque * self.stat_attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)

    def Touche_loin(self,game) : 
        for enemy in game.player_units:
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 3 <= distance <= 5 :  

                degat = self.puissance_attaque * self.stat_attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)
                break

    def degat_subit(self,monstre,degat):
        """Fonction qui permet de calculer le dommage final en suivant du type de l'attaquant """
        if monstre.type == "Mage": 
            degat_final = degat *1.25
        elif monstre.type == "Vampire" : 
            degat_final = degat*1.25
        elif monstre.type == "Guerrier": 
            degat_final = degat *0.75
        else : 
            degat_final = degat 
        
        return degat_final-(degat*self.stat_defense)
    
    def attaque(self,attaque_choisie,game):
        
        if attaque_choisie == "Peur":

            self.Peur(game)
        elif attaque_choisie == "Onde de choc" : 
            self.Onde_de_choc(game)
        elif attaque_choisie == "Touche loin" : 
            self.Touche_loin(game)


class Roi_enemy(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 'enemy', image_roi ,0.8,1,2)
        self.liste_attaque = ["Peur", "Onde de choc ", "Invoquer"]
        self.type = "Roi"
        self.health = 150
        self.max_health = 150


    def Peur(self,game) : 
        for enemy in game.player_units:
            """Fait peur au joueur se trouvant dans un rayon de 3 block au alentour, fait baisser leur attaque """
            
            if enemy.stat_attaque - 0.1 <= 0.1 : # pour eviter d'avoir un puissance d'attaque nuls et de ne plus pouvoir attaquer
                    enemy.stat_attaque = 0.1
            else : 
                enemy.stat_attaque -= 0.1  

    def Onde_de_choc(self,game) : 
        for enemy in game.player_units:
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if 0 <= distance <= 3:  

                degat = self.puissance_attaque * self.stat_attaque
                degat_final = enemy.degat_subit(self, degat)
                enemy.update_health(degat_final)
                
                if not enemy.en_vie:
                    game.enemy_units.remove(enemy)

    def Invoquer(self,game) : 
        game.create_monsters_in_room(self, 5)

    def degat_subit(self,monstre,degat):
        """Fonction qui permet de calculer le dommage final en suivant du type de l'attaquant """
        if monstre.type == "Mage": 
            degat_final = degat *0.75
        elif monstre.type == "Vampire" : 
            degat_final = degat*0.75
        elif monstre.type == "Guerrier": 
            degat_final = degat *1.25
        else : 
            degat_final = degat 
        
        return degat_final-(degat*self.stat_defense)
    
    def attaque(self,attaque_choisie,game):
        
        if attaque_choisie == "Peur":

            self.Peur(game)
        elif attaque_choisie == "Onde de choc" : 
            self.Onde_de_choc(game)
        elif attaque_choisie == "Invoquer" : 
            self.Invoquer(game)
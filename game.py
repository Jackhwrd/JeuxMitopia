import pygame 
import random
from collections import deque

from unit import *
from game_map import *
from image import *
from classes import *

walls = mur()
rooms = generate_rooms(salles)


class Game:
    

    def __init__(self, screen,player_classe):
        """
        Initialise le jeu avec les paramètres nécessaires.
        """
        self.In_Game = False
        self.screen = screen
        self.enemy_images = [image_mechant_guerier, image_mechant_vampire, image_mechant_mage]
        self.player_class = player_classe # liste des classes des joueurs 

        self.walls = mur()
        self.salles = salles
        self.rooms = generate_rooms(salles)
        self.objects = generate_objects()
        self.cases_reg = generate_cases()
        self.traps = generate_traps()


    def bfs_reachable(self, selected_unit):
            visited = np.zeros((HEIGHT,WIDTH))
            queue = deque([(selected_unit.x, selected_unit.y, 0)])  
            visited[selected_unit.x, selected_unit.y] = True
            reachable = []
            k = 0

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4 directions
    
            while queue:
                x, y, dist = queue.popleft()
        
                if dist > selected_unit.vitesse:  
                    continue

                print(x,y,dist)

                reachable.append((x, y))

            # Explore toute les directions
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and not visited[ny, nx] and not self.is_wall(nx,ny) and not self.is_occupied_by_unit(nx,ny):
                        visited[ny, nx] = True
                        queue.append((nx, ny, dist + 1))
    
            return reachable   
        
    def distance_to_all_units(self, selected_unit):
        print("calcul de distance")
        distances = {}  # Dictionnaire pour stocker les distances de toutes les unités
        visited = np.zeros((HEIGHT, WIDTH))  # Cases visitées
        queue = deque([(selected_unit.x, selected_unit.y, 0)])  # Point de départ (x, y, distance)
        visited[selected_unit.y, selected_unit.x] = True
        player_units = []
        k = 0
        for unit in self.player_units:
            print(unit.x, unit.y)

        # Directions pour se déplacer sur la grille (haut, bas, gauche, droite)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4 directions
        searching = True
        while searching:
            x, y, dist = queue.popleft()
            print(x,y,dist)

            # Ajouter la position de l'unité et sa distance au dictionnaire 
            if self.is_occupied_by_player(x, y):
                distances[(x, y)] = dist
                print("unité découverte")
                print(x,y)
                player_units.append(self.unit_at_position(x,y))
                print(player_units)
                if len(player_units) == len(self.player_units):
                    searching = False
                    continue

            # Explorer toutes les directions (haut, bas, gauche, droite)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and not visited[ny, nx] and not self.is_wall(nx, ny):
                    visited[ny, nx] = True
                    queue.append((nx, ny, dist + 1))
            k += 1
        print(k)
        print(distances)
        return distances

    def calculate_preference_weight(self, selected_unit, target_unit):
        """Calculer le poids de préférence en fonction des types d'unités."""
        if selected_unit.type == target_unit.type:
            return 1  # Pas de biais si même type
        elif selected_unit.type == "Mage" and target_unit.type == "Vampire":
            return 1.5  # Le vert préfère le rouge
        elif selected_unit.type == "Vampire" and target_unit.type == "Guerrier":
            return 1.5  # Le rouge préfère le bleu
        elif selected_unit.type == "Guerrier" and target_unit.type == "Mage":
            return 1.5  # Le bleu préfère le vert
        else:
            return 0.5  # Paires les moins préférées (vert vs bleu, rouge vs vert, etc.)

    def select_target_unit(self, selected_unit):
        print("sélection de cible")
        distances = self.distance_to_all_units(selected_unit)

        # Extraire les unités et leurs distances
        units = list(distances.keys())  # Unités accessibles
        dist_values = list(distances.values())  # Distances correspondantes

        # Inverser les distances (les unités plus proches doivent avoir un poids plus élevé)
        max_distance = max(dist_values) if dist_values else 1
        weights = [max_distance + 1 - dist for dist in dist_values]  # Inverser les distances pour la probabilité
        print(weights)

        # Calculer les poids de préférence en fonction du type d'unité
        preference_weights = [
            self.calculate_preference_weight(selected_unit, self.unit_at_position(unit[0],unit[1])) for unit in units
        ]
        print(preference_weights)

        # Poids finaux : combiner les poids de distance et les poids de préférence
        final_weights = [weights[i] * preference_weights[i] for i in range(len(weights))]
        print(final_weights)

        # Normaliser les poids finaux pour que leur somme soit égale à 1
        total_weight = sum(final_weights)
        normalized_weights = [w / total_weight for w in final_weights]
        print(normalized_weights)

        # Sélectionner une unité cible en fonction des poids calculés
        target_unit = random.choices(units, weights=normalized_weights, k=1)[0]
        print(target_unit)
        return target_unit
    

    def get_best_adjacent_move(self, base_unit, target_unit):
        """Choisir la meilleure case adjacente pour se déplacer vers l'unité cible."""
        # Directions pour se déplacer sur la grille (haut, bas, gauche, droite)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4 directions (pas de diagonales)

        # Obtenir la position actuelle de l'unité de base
        x, y = base_unit.x, base_unit.y

        # Trouver la position de l'unité cible
        target_x, target_y = target_unit.x, target_unit.y

        # Initialiser le meilleur mouvement et sa distance
        best_move = None
        min_distance = float('inf')

        # Explorer toutes les directions pour trouver la case adjacente la plus proche de la cible
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Vérifier si la nouvelle position est dans les limites et n'est pas un mur
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and not self.is_wall(nx, ny) and not self.is_occupied_by_unit(nx,ny):
                    # Vérifier si la position actuelle est plus proche de la cible que le meilleur mouvement précédent
                target_distance = abs(target_x - nx) + abs(target_y - ny)  # Distance de Manhattan à la cible
                if target_distance < min_distance:
                    min_distance = target_distance
                    best_move = (dx, dy)

        return best_move
                
    def handle_player_turn(self):
        """Tour du joueur"""
        for rang_joueur, selected_unit in enumerate (self.player_units):

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            #selected_unit.is_selected = True
            selecting_attack = False  # Flag pour savoir si on est dans le menu d'attaque
            current_option = 0  # Option actuelle
            selected_attack = 0  # Attaque actuellement sélectionnée
            self.flip_display()
            
            while not has_acted: # tant que le tour du joueur n'est pas fini
                #affichage du numéros de joueur qui doit jouer 

                phrase = f"Joueur {rang_joueur + 1 }, à toi de jouer !"
                texte = font_affi_joueur.render(phrase, True, WHITE)
                text_rect = texte.get_rect(center=(540, 20))  # Espacement vertical entre les options
                self.screen.blit(texte, text_rect.topleft)
                

                # Boucle principale d'événements
                for event in pygame.event.get():
                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:
                        # Si on n'est pas dans le menu d'attaque, afficher les options principales
                        if not selecting_attack:
                            # Déplacement du curseur entre "Avancer" et "Attaquer"
                            if event.key == pygame.K_DOWN:
                                current_option = (current_option + 1) % 2
                            elif event.key == pygame.K_UP:
                                current_option = (current_option - 1) % 2
                            
                            # Si l'option "Attaquer" est sélectionnée
                            if event.key == pygame.K_RETURN and current_option == 1:
                                selecting_attack = True  # On passe dans le menu d'attaque
                                self.flip_display()

                            # Si l'option "Avancer" est sélectionnée, on déplace l'unité
                            if event.key == pygame.K_RETURN and current_option == 0:
                                self.move_unit_multiple(selected_unit)
                                self.flip_display()
                                has_acted = True 
                            
                        # Si on est dans le menu d'attaque
                        else:
                            # Sélection des attaques
                            if event.key == pygame.K_DOWN:
                                selected_attack = (selected_attack + 1) % len(selected_unit.liste_attaque)
                            elif event.key == pygame.K_UP:
                                selected_attack = (selected_attack - 1) % len(selected_unit.liste_attaque)

                            # Si l'attaque est confirmée
                            if event.key == pygame.K_RETURN:
                            
                                has_acted = self.gestion_attaque(selected_unit,selected_attack)
                                #selected_unit.is_selected = not has_acted
                                selecting_attack = has_acted
                                self.flip_display()
                                
                         # Affichage des options principales (Avancer ou Attaquer)
                    if not selecting_attack:
                        options = ["Avancer", "Attaquer"]
                        for i, option in enumerate(options):
                            color = BLUE if i == current_option else WHITE
                            texte = font.render(option, True, color)
                            text_rect = texte.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 70))
                            self.screen.blit(texte, text_rect)
                    
                    # Affichage des attaques si l'option "Attaquer" est choisie
                    else:
                        for i, attack in enumerate(selected_unit.liste_attaque):
                            color = BLUE if i == selected_attack else WHITE
                            texte = font.render(attack, True, color)
                            text_rect = texte.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 70))
                            self.screen.blit(texte, text_rect)

                # Gestion des touches du clavier
                if event.type == pygame.KEYDOWN:

                    # Déplacement (touches fléchées)
                    dx, dy = 0, 0
                    if event.key == pygame.K_LEFT:
                        dx = -1
                        if selected_unit.x == 0 and selected_unit.y == GRID_SIZE_V - 1:
                            target_pos = (GRID_SIZE_H - 1, 0)  # Par exemple, coordonnées de téléportation
                            teleport_unit(selected_unit, target_pos, self.rooms, self.salles)
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                        # Téléportation si en haut à droite
                        if selected_unit.x == GRID_SIZE_H - 1 and selected_unit.y == 0:
                            target_pos = (0, GRID_SIZE_V - 1)  # Par exemple, coordonnées de téléportation
                            teleport_unit(selected_unit, target_pos, self.rooms, self.salles)
                            #self.flip_display()
                            #has_acted = True
                            continue
                    elif event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1
                    
                    new_x = selected_unit.x + dx
                    new_y = selected_unit.y + dy
                    if not (0 <= new_x < GRID_SIZE_H and 0 <= new_y < GRID_SIZE_V):
                        print("Vous ne pouvez pas sortir des limites de la carte !")
                        continue
                    
                    # Vérification des cases de régénération
                    for cas in self.cases_reg:
                        if cas.x == new_x and cas.y == new_y:
                            print(f"Régénération de l'unité {selected_unit}")
                            cas.appliquer_effet(selected_unit, self)  # Déclenche les effets du piège
                            
                            break

                    # Vérification des pièges
                    #trap_found = False
                    for trap in self.traps:
                        if trap.x == new_x and trap.y == new_y:
                            print(f"Unité {selected_unit} a rencontré un piège {trap.trap_type}.")
                            trap.is_active = True
                            #trap_found = True  # Indique que le mouvement est bloqué
                            #print(f"Le piège {trap.trap_type} s'active sur {selected_unit}.")
                            trap.trigger(selected_unit)  # Déclenche les effets du piège
                            #trap.block_movement :  # Si le piège bloque le mouvement
                            dx, dy = 0, 0
                            break
                    
                    
                    # Si la touche entrer est appuyée, essayer de ramasser un objet
                    if event.key == pygame.K_RSHIFT:  # Touche entrer du pavé numérique
                        for obj in self.objects:
                            if obj.x == selected_unit.x and obj.y == selected_unit.y:
                                print(f"Vous avez ramassé {obj.name} !")
                                obj.collected = True  # L'objet est ramassé
                                self.objects.remove(obj)  # Retirer de la carte
                                
                                # Ajoutez l'objet à la liste `has_object` (si elle existe, sinon initialisez-la)
                                if not hasattr(selected_unit, 'has_object'):
                                    selected_unit.has_object = []  # Si la liste n'existe pas, créez-la

                                selected_unit.has_object.append(obj)  # Ajouter l'objet à la liste
                                print(f"L'objet dans has_object : {selected_unit.has_object[-1].name}")  # Affiche le dernier objet collecté
                                break 
                    
                        
                    # Vérifier les collisions avec les murs
                    proposed_rect = pygame.Rect(
                        new_x * CELL_SIZE,
                        new_y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                    )
                    if any(proposed_rect.colliderect(wall) for wall in self.walls):
                        print("Collision détectée ! Mouvement annulé.")
                        # Collision détectée : ne pas appliquer le déplacement
                        continue

                    # Vérifier si le joueur tente d'entrer dans une salle
                    room_id = (
                        self.rooms[new_x, new_y]
                        if (0 <= new_x < GRID_SIZE_H and 0 <= new_y < GRID_SIZE_V)
                        else 0
                    )
                    salle = next((s for s in salles if s.id == room_id), None)

                    # Si la salle est ouverte
                    if salle:
                        if salle.verifier_conditions(selected_unit):
                            selected_unit.x, selected_unit.y = new_x, new_y
                            print(f"Vous êtes entré dans la salle {salle.id}.")
                        else:
                            print(f"Accès refusé à la salle {salle.id}.")

                    # Si le joueur entre dans une salle, vérifier les conditions
                    if salle:
                        if salle.verifier_conditions(selected_unit):
                            selected_unit.x, selected_unit.y = new_x, new_y
                            print(f"Vous êtes entré dans la salle {salle.id}.")
                        else:
                            print(f"Accès refusé à la salle {salle.id}.")
                    else:
                        # Pas de salle : déplacer normalement
                        selected_unit.x, selected_unit.y = new_x, new_y
                        
                    self.flip_display()
                    # Attaque (touche espace) met fin au tour
                    if event.key == pygame.K_SPACE:
                        for enemy in self.enemy_units:
                            if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                selected_unit.attack(enemy)
                                if enemy.health <= 0:
                                    self.enemy_units.remove(enemy)
                                if selected_unit.puissance_attaque >= ATTAQUE_DESTRUCTRICE :
                                    self.mur.remove()

                                has_acted = True
                                selected_unit.is_selected = False

                # Affichage des options principales (Avancer ou Attaquer)
                if not selecting_attack:
                    options = ["Avancer", "Attaquer"]
                    for i, option in enumerate(options):
                        color = BLUE if i == current_option else WHITE
                        texte = font.render(option, True, color)
                        text_rect = texte.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 70))
                        self.screen.blit(texte, text_rect)
                
                # Affichage des attaques si l'option "Attaquer" est choisie
                else:
                    for i, attack in enumerate(selected_unit.liste_attaque):
                        color = BLUE if i == selected_attack else WHITE
                        texte = font.render(attack, True, color)
                        text_rect = texte.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 70))
                        self.screen.blit(texte, text_rect)

                # Mise à jour de l'affichage
                pygame.display.flip()

         

    def gestion_attaque(self, selected_unit,selected_attack):
        if selected_attack == 0: 
            print(f'{selected_unit.liste_attaque[0]}') 
            Attack = selected_unit.vise_attaque(selected_unit.liste_attaque[0],self)
            print(f"Résultat de vise_attaque : {Attack}")
            if Attack :
                print(f'Cible trouvée, exécution de l attaque')
                selected_unit.execute_attaque(self, Attack)
        elif selected_attack == 1:  
            Attack = selected_unit.vise_attaque(selected_unit.liste_attaque[1],self)
            print(f'{selected_unit.liste_attaque[1]}')
            return True
        elif selected_attack == 2 : 
            Attack = selected_unit.vise_attaque(selected_unit.liste_attaque[2],self)
            print(f'{selected_unit.liste_attaque[2]}')
            return True
        
        running = True # utilise BFS pathfinding algorithme pour trouver les positions atteignable par l'unité 
        starting_x,starting_y = selected_unit.x,selected_unit.y

            # Stocker les coordonnées initiales de l'unité pour calculer la distance parcourue
        while running:
            self.flip_display(None, Attaque = Attack)  # Mettre à jour l'affichage

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    # Terminer le déplacement avec la touche Espace
                    if event.key == pygame.K_SPACE:
                        print("Attack terminée.")
                        running = False
                        return False

                    if event.key == pygame.K_RETURN:
                        pass

                    # Calcul du déplacement
                    dx, dy = 0, 0
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1

                    # Calcul des nouvelles coordonnées
                    new_x = Attack.x + dx
                    new_y = Attack.y + dy

                    # Vérification des limites de déplacement
                    distance = abs(new_x - starting_x) + abs(new_y - starting_y)
                    if distance > Attack.range:
                        print("Déplacement trop loin ! Mouvement annulé.")
                        continue

                    # Vérifier les collisions avec les murs

                    if self.is_wall(new_x, new_y) and not Attack.walls:
                        print("Collision avec un mur ! Mouvement annulé.")
                        continue

                    # Déplacement valide : mettre à jour la position de l'unité
                    Attack.move(dx,dy)
        print("attaque terminé")
        return True

    
    def move_unit_multiple(self, selected_unit):
        """Permet à une unité de se déplacer plusieurs fois jusqu'à ce que l'utilisateur décide d'arrêter avec Espace."""
        running = True
        Rlist = self.bfs_reachable(selected_unit) # utilise BFS pathfinding algorithme pour trouver les positions atteignable par l'unité 
        print(Rlist)
        
        # Stocker les coordonnées initiales de l'unité pour calculer la distance parcourue
        while running:
            self.flip_display(Rlist)  # Mettre à jour l'affichage

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    # Terminer le déplacement avec la touche Espace
                    if event.key == pygame.K_SPACE:
                        print("Déplacement terminé.")
                        running = False
                        break

                    # Calcul du déplacement
                    dx, dy = 0, 0
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1

                    # Calcul des nouvelles coordonnées
                    new_x = selected_unit.x + dx
                    new_y = selected_unit.y + dy

                    # Vérification des limites de déplacement
                    if not (new_x,new_y) in Rlist:
                        print("Déplacement trop loin ! Mouvement annulé.")
                        continue

                    # Vérifier les collisions avec les murs
                    if self.is_wall(new_x, new_y):
                        print("Collision avec un mur ! Mouvement annulé.")
                        continue

                    # Vérifier si la case est occupée par une autre unité
                    if self.is_occupied_by_unit(new_x, new_y):
                        print("La case est déjà occupée ! Mouvement annulé.")
                        continue

                    # Vérifier si le joueur entre dans une salle
                    if 0 <= new_x < self.rooms.shape[0] and 0 <= new_y < self.rooms.shape[1]:  # Vérifie les limites
                        room_id = self.rooms[new_x, new_y]
                    else:
                        room_id = None

                    salle = next((s for s in salles if s.id == room_id), None)

                    # Déplacer l'unité ou afficher un message si elle ne peut pas entrer
                    if salle:
                        if salle.verifier_conditions(selected_unit):
                            selected_unit.x, selected_unit.y = new_x, new_y
                            print(f"Vous êtes entré dans la salle {salle.id}.")
                        else:
                            print(f"Accès refusé à la salle {salle.id}.")
                    else:
                        # Déplacement normal
                        selected_unit.x, selected_unit.y = new_x, new_y

                    print(f"Unité déplacée en ({new_x}, {new_y}).")

                    # Vérification pour ramasser des objets
                    for obj in self.objects:
                        if obj.x == new_x and obj.y == new_y:
                            print(f"Vous avez ramassé {obj.name} !")
                            obj.collected = True
                            self.objects.remove(obj)
                            if not hasattr(selected_unit, 'has_object'):
                                selected_unit.has_object = []
                            selected_unit.has_object.append(obj)
                            print(f"Inventaire : {selected_unit.has_object[-1].name}.")
                            break
                       
            

    def is_wall(self, x, y):
        """Vérifie si une case donnée contient un mur."""
        for wall in walls:
            if wall.collidepoint(x * CELL_SIZE, y * CELL_SIZE):
                return True
        return False
    
    def is_occupied_by_unit(self, x, y):
        """Vérifie si une case est occupée par une unité."""
        for unit in self.player_units + self.enemy_units:
            if unit.x == x and unit.y == y:
                return True
        return False

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""

        for enemy in self.enemy_units:
            if enemy.type == "Roi":  # Le roi se déplace seulement si un joueur est dans l'arène finale
                if self.peu_jouer_roi(salles):  

                    # Déplacement aléatoire vers un joueur
                    target = random.choice(self.player_units)
                    dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
                    dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0

                    new_x, new_y = enemy.x + dx, enemy.y + dy
                    
                    if 0 <= new_x < GRID_SIZE_H and 0 <= new_y < GRID_SIZE_V and not self.is_wall(new_x, new_y) and not self.is_occupied_by_unit( new_x, new_y):
                        enemy.move(dx, dy)
                    #choix d'une attaque aléatoire
                    attaque_choix = random.randint(0, 2)
                    enemy.attaque(self, enemy.liste_attaque[attaque_choix])
                else:
                    continue

            else:  # Pour les autres ennemis
                # Déplacement aléatoire vers un joueur
                target = random.choice(self.player_units)
                dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
                dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0

                new_x, new_y = enemy.x + dx, enemy.y + dy
                
                if 0 <= new_x < GRID_SIZE_H and 0 <= new_y < GRID_SIZE_V and not self.is_wall(new_x, new_y) and not self.is_occupied_by_unit( new_x, new_y):
                    enemy.move(dx, dy)

                attaque_choix = random.randint(0, 2)
                enemy.attaque(self, enemy.liste_attaque[attaque_choix])

            


    def flip_display(self, Rlist=None, Attaque= None):
        """Affiche le jeu."""

        # Effacer l'écran (en dehors de la boucle principale pour éviter les flashs)
        self.screen.fill(RED)

        # Affiche la grille
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                
                # Obtenir la couleur de la cellule
                color = get_cell_color(grid_x, grid_y, self.rooms, self.walls, salles)
                    
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect)

                # Ne pas dessiner la grille pour les cases de murs
                if self.is_wall(grid_x, grid_y):
                    pygame.draw.rect(self.screen, BLACK, rect)  # Dessiner les murs

                pygame.draw.rect(self.screen, BLACK, rect, 1)

        # Affiche les unités
        for unit in self.player_units + self.enemy_units :
            unit.draw(self.screen)
            unit.update_health_bar(self.screen)
        
        # Affiche les objets
        for obj in self.objects:
            obj.draw(self.screen)
        
        # Affiche les cases de régénération
        for cas in self.cases_reg:
            cas.draw(self.screen)
        
        # Affiche les pièges
        for tra in self.traps:
            tra.draw(self.screen)
        
        # Afficher les attaques si nécessaire

        # Rafraîchissement de l'écran
        if Rlist != None:
            for x, y in Rlist:
                rect_x = x * CELL_SIZE
                rect_y = y * CELL_SIZE
                pygame.draw.rect(self.screen, YELLOW, (rect_x, rect_y, CELL_SIZE, CELL_SIZE), 1)

        if Attaque != None:
            Attaque.draw(self.screen)

        pygame.display.flip()

    def game_over(self) :
        som = 0
        for unit in self.player_units : 
            if unit.en_vie == False : 
                som+=1
        if som == 3 :
            self.In_Game = False
        
    def victoire(self) : 
        som = 0
        for unit in self.player_units : 
            if unit.en_vie == False : 
                som+=1
        if som < 3 and self.roi.en_vie :
            self.In_Game = False
    
    
    
    def is_player_in_room(self, room_id):
        """
        Vérifie si un joueur est dans la salle spécifiée.
        
        Paramètre :
            room_id (int): Identifiant de la salle à vérifier.
        
        Retourne :
            bool: True si un joueur est dans la salle, sinon False.
        """
        for player in self.player_units:  # Assumes self.player_units contient les unités des joueurs
            if player.room_id == room_id:  # Assuming player has a room_id attribute
                return True
        return False

    def spawn_monsters(self, salles):
        """
        Fait apparaître des monstres dans les salles où il y a des joueurs, sauf dans l'arène.
        """
        # Liste des salles où les joueurs se trouvent
        player_rooms = self.get_player_rooms(salles)
        
        for salle in player_rooms:  # On parcourt seulement les salles où des joueurs se trouvent
            # Ne pas générer de monstres dans l'arène
            if salle.id == 5:  # Id de l'arène, à ajuster si nécessaire
                print(f"Pas de monstres dans la salle {salle.id} (l'arène).")
                continue
            
            self.create_monsters_in_room(salle)

    def get_player_rooms(self, salles):
        """
        Détecte dans quelles salles se trouvent les joueurs.
        
        Paramètre :
            salles (list): Liste des salles disponibles dans le jeu.
        
        Retourne :
            list: Une liste des salles où des joueurs sont présents.
        """
        player_rooms = []
        for salle in salles:
            for player in self.player_units:  
                # Vérifie si le joueur est dans cette salle (en fonction de ses coordonnées x et y)
                if salle.x_min <= player.x <= salle.x_max and salle.y_min <= player.y <= salle.y_max:
                    if salle not in player_rooms:
                        player_rooms.append(salle)
        return player_rooms
    
    def peu_jouer_roi(self, salles):
        player_rooms = self.get_player_rooms(salles)
        for salle in player_rooms : 
            if salle.id == 5 : # un joueur est dans l'arene 
                return True 
        return False 

    def create_monsters_in_room(self, salle):
        """
        Crée des monstres de manière aléatoire dans la salle donnée, sauf si c'est l'arène.
        
        Paramètre :
            salle (salle): La salle où les monstres seront créés.
        """
        # Ne pas générer de monstres dans l'arène
        if salle.id == 5:  # Id de l'arène, à ajuster si nécessaire
            print(f"Pas de monstres dans la salle {salle.id} (l'arène).")
            return

        # Générer des monstres aléatoires avec un maximum de 6 ennemis
        max_monsters = 6
        if len(self.enemy_units) >= max_monsters:
            print("Trop de monstres sur le terrain ! Aucun nouveau monstre n'a été ajouté.")
            return

        possible_classes = [Mage_enemy, Vampire_enemy, Guerrier_enemy]
        new_monsters = []
        
        for _ in range(random.randint(1, 3)):  # Entre 1 et 3 nouveaux monstres
            if len(self.enemy_units) + len(new_monsters) >= max_monsters:
                break

            # Générer des coordonnées aléatoires pour les monstres dans les limites de la salle
            x, y = random.randint(salle.x_min, salle.x_max), random.randint(salle.y_min, salle.y_max)
            while self.is_wall(x, y) or self.is_occupied_by_unit(x, y):
                x, y = random.randint(salle.x_min, salle.x_max), random.randint(salle.y_min, salle.y_max)

            # Choisir le type de monstre et ajouter au jeu
            monster_class = random.choice(possible_classes)
            new_monsters.append(monster_class(x, y))

        # Ajouter les nouveaux monstres au jeu
        self.enemy_units.extend(new_monsters)
        print(f"{len(new_monsters)} monstres ont été ajoutés dans la salle {salle.id}.")

        
    def debut_jeu(self):
        self.player_units = []
        for i, player_class in enumerate(self.player_class):
            if player_class == "Mage":
                    self.player_units.append(Mage_player(i,0))
            elif player_class == "Vampire":
                    self.player_units.append(Vampire_player(i,0))
            elif player_class == "Guerrier":
                    self.player_units.append(Guerrier_player(i,0))

        self.enemy_units = [Vampire_enemy(6,6),
                            Mage_enemy(7,6),
                            Guerrier_enemy(8,6),
                            Roi_enemy(37,21)]
       
    def En_jeu(self) : 
        self.debut_jeu()
        self.In_Game = True
        while True:
            self.handle_player_turn()
            self.handle_enemy_turn()
            self.spawn_monsters(salles)
            self.game_over()
            
   
def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Test du jeu de stratégie")

    # Instanciation du jeu
    Perso = ["Mage","Guerrier","Vampire"]
    game = Game(screen, Perso)

    # Boucle principale du jeu
    game.En_jeu()
        
if __name__ == "__main__":
    main()

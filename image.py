import pygame 
pygame.font.init()

# Constantes
GRID_SIZE_V = 24
GRID_SIZE_H = 40
CELL_SIZE = 30
WIDTH = GRID_SIZE_H * CELL_SIZE
HEIGHT = GRID_SIZE_V * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)           #base RVB
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


# Constantes
GRID_SIZE_V = 24
GRID_SIZE_H = 40
CELL_SIZE = 30
WIDTH = GRID_SIZE_H * CELL_SIZE
HEIGHT = GRID_SIZE_V * CELL_SIZE
FPS = 30
drop_width = 8
drop_height = 11

# Couleurs
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
NOIR = (0,0,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)           #base RVB
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
OLIVE = (128, 128, 0)
BROWN = (131, 118, 105)
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (255, 255, 153)
KAKI = (140, 130, 80)
MAGE = (182,37,207)
GUERRIER = (138,148,163)
VAMPIRE = (161,0,0)
background_color = (60, 63, 60)
health_color = (111, 210, 46)

#permet l'import de toute les images du jeu
arriere_plan = pygame.image.load("image/ecran_titre.JPG")
image_croque_minou = pygame.image.load("image/Croque_minou.png")
image_roi = pygame.image.load("image/roi.png")
image_status = pygame.image.load("image/mechant_status.png")
image_mechant_guerier = pygame.image.load("image/mechant_guerier.png")
image_mechant_vampire = pygame.image.load("image/mechant_vampire.png")
image_mechant_mage = pygame.image.load("image/mechant_mage.png")
image_guts = pygame.image.load("image/guts.jpeg")
image_vampire = pygame.image.load("image/vampire.jpg")
image_viseur = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
pygame.draw.circle(image_viseur, RED, (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE//2, width=3)
pygame.draw.line(image_viseur, BLACK, (0, CELL_SIZE//2 - 1),(CELL_SIZE, CELL_SIZE//2 - 1), 2)  # Ligne Horizontale
pygame.draw.line(image_viseur, BLACK, (CELL_SIZE//2 - 1, 0),(CELL_SIZE//2 - 1, CELL_SIZE), 2)  # Ligne Verticale
blood_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)

#dessin de l'éllipse
pygame.draw.ellipse(blood_surface, VAMPIRE, (CELL_SIZE//2 - drop_width // 2, CELL_SIZE//2 - drop_height // 2, drop_width, drop_height // 2))

#dessin du triangle
triangle_points = [
    (CELL_SIZE//2 + 1,3),  # bottom point (centered)
    (CELL_SIZE//2 - drop_width // 2, CELL_SIZE//2 - drop_height//2 + 1),  # left point
    (CELL_SIZE//2 + drop_width // 2, CELL_SIZE//2 - drop_height//2 + 1)  # right point
]
pygame.draw.polygon(blood_surface, VAMPIRE, triangle_points) #ajout les deux ensemble (tentative de dessiner une goutte de sang, pas trop réussit)


zone_vampiriser = pygame.Surface((CELL_SIZE*5, CELL_SIZE*5), pygame.SRCALPHA)
pygame.draw.rect(zone_vampiriser, VAMPIRE, (0, 0, CELL_SIZE*5, CELL_SIZE*5), width = 2)

image_selectionner_allié = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
pygame.draw.rect(image_selectionner_allié, GREEN, (0, 0, CELL_SIZE, CELL_SIZE), width = 3)



# Initialisation de la police
font = pygame.font.Font("acadian_runes/police.ttf", 80)  

# Initialisation de la police pour les crédits (pour que le texte soit plus petit)
font_game = pygame.font.Font("acadian_runes/police.ttf", 48)
font_credit = pygame.font.Font("acadian_runes/police.ttf", 40)  
font_j = pygame.font.Font("acadian_runes/police.ttf", 20)
font_affi_joueur = pygame.font.Font("acadian_runes/police.ttf", 30)





import pygame 
pygame.font.init()

#permet l'import de toute les images du jeu
arriere_plan = pygame.image.load("image/ecran_titre.JPG")
image_croque_minou = pygame.image.load("image/Croque_minou.png")
image_roi = pygame.image.load("image/roi.png")
image_status = pygame.image.load("image/mechant_status.png")
image_mechant_guerier = pygame.image.load("image/mechant_guerier.png")
image_mechant_vampire = pygame.image.load("image/mechant_vampire.png")
image_mechant_mage = pygame.image.load("image/mechant_mage.png")



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

# Initialisation de la police
font = pygame.font.Font("acadian_runes/police.ttf", 80)  

# Initialisation de la police pour les crédits (pour que le texte soit plus petit)
font_game = pygame.font.Font("acadian_runes/police.ttf", 48)
font_credit = pygame.font.Font("acadian_runes/police.ttf", 40)  
font_j = pygame.font.Font("acadian_runes/police.ttf", 20)

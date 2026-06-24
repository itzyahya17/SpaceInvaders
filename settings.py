import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WIDTH, HEIGHT = 1280, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Space Invader")

ENEMY_SHIP_GREEN = pygame.image.load(os.path.join(BASE_DIR, "assets", "enemy_ship_green.png"))
ENEMY_SHIP_RED   = pygame.image.load(os.path.join(BASE_DIR, "assets", "enemy_ship_red.png"))
ENEMY_SHIP_BLUE  = pygame.image.load(os.path.join(BASE_DIR, "assets", "enemy_ship_blue.png"))

PLAYER_SHIP_ORANGE = pygame.image.load(os.path.join(BASE_DIR, "assets", "player_ship_orange.png"))

LASER_GREEN  = pygame.image.load(os.path.join(BASE_DIR, "assets", "laser_green.png"))
LASER_RED    = pygame.image.load(os.path.join(BASE_DIR, "assets", "laser_red.png"))
LASER_BLUE   = pygame.image.load(os.path.join(BASE_DIR, "assets", "laser_blue.png"))
LASER_ORANGE = pygame.image.load(os.path.join(BASE_DIR, "assets", "laser_orange.png"))

BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join(BASE_DIR, "assets", "background_space.png")),
    (WIDTH, HEIGHT)
)

BG = BACKGROUND

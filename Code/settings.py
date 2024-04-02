import pygame

vertical_tile_number = 11
tile_size = 64
screen_height = vertical_tile_number * tile_size
screen_width = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
clock = pygame.time.Clock()
click = False

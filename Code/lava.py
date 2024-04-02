from settings import screen_width
import pygame
from Tiles import AnimatedTile


class Lava:
    def __init__(self, top, level_width):
        lava_start = -screen_width
        lava_width = 220
        tile_x_amount = int((level_width + screen_width) / lava_width)
        self.lava_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * lava_width + lava_start
            y = top
            sprite = AnimatedTile(220, x, y, '../Graphics/Decorations/Lava')
            self.lava_sprites.add(sprite)

    def draw(self, surface, shift):
        self.lava_sprites.update(shift)
        self.lava_sprites.draw(surface)

import pygame
from support import folder_import


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.34
        if type == 'jump':
            self.frames = folder_import('../Graphics/Character/dust_particles/jump')
        if type == 'land':
            self.frames = folder_import('../Graphics/Character/dust_particles/land')
        if type == 'explosion':
            self.frames = folder_import('../Graphics/Enemies/explosion')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift

import pygame
from support import folder_import
from math import sin


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health, sound):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # dust particles
        self.import_running_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # Player movement
        self.speed = 8
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft, (33, self.rect.height))

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # Sound effects
        self.jump_sound = pygame.mixer.Sound('../Music/effects/jump.wav')
        self.jump_sound.set_volume(0.1)
        self.hit_sound = pygame.mixer.Sound('../Music/effects/player_damage.mp3')
        self.sound = sound
        if not self.sound:
            self.jump_sound.set_volume(0)
            self.hit_sound.set_volume(0)

        # health
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 1000
        self.hurt_time = 0

    def import_character_assets(self):
        path = '../Graphics/Character/'
        self.animations = {'idle': [], 'fall': [], 'run': [], 'jump': []}

        for animation in self.animations.keys():
            complete_path = path + animation
            self.animations[animation] = folder_import(complete_path)

    def animate_player(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = pygame.transform.scale(image, (40, 48))
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.scale(pygame.transform.flip(image, True, False), (40, 48))
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def play_dust(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def import_running_particles(self):
        self.dust_run_particles = folder_import('../Graphics/Character/dust_particles/run')

    def get_keyboard_inputs(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
                self.facing_right = True

    def get_damage(self):
        if not self.invincible:
            self.change_health(-25)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
            self.hit_sound.play()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.get_keyboard_inputs()
        self.get_status()
        self.animate_player()
        self.play_dust()
        self.invincibility_timer()
        self.wave_value()

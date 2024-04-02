import pygame
from support import import_csv_layout, cutout_graphics
from settings import tile_size, screen_width, screen_height
from Tiles import Tile, StaticTile, Crate, Coin, AnimatedTile
from Enemy import Enemy
from player import Player
from particles import ParticleEffect
from lava import Lava
from game_modules import respawn, end, completed
from game_data import Level_0
from overlay import overlay

screen = pygame.display.set_mode((screen_width, screen_height))


class Level:
    def __init__(self, level_data, surface, lives, coins, sound):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # Sound Effects

        self.coin_sound = pygame.mixer.Sound('../Music/effects/coin.wav')
        self.coin_sound.set_volume(0.1)
        self.enemy_stomp = pygame.mixer.Sound('../Music/effects/stomp.wav')
        self.enemy_stomp.set_volume(0.4)
        self.hit_sound = pygame.mixer.Sound('../Music/effects/player_damage.mp3')
        self.sound = sound
        if not self.sound:
            self.coin_sound.set_volume(0)
            self.enemy_stomp.set_volume(0)
            self.hit_sound.set_volume(0)

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.max_health = 100
        self.current_health = 100
        self.coins = coins
        self.player_setup(player_layout, self.change_health)
        self.dead = False
        self.lives = lives

        # user overlay
        self.overlay = overlay(self.display_surface)

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # enemy explosion particles
        self.explosion_sprites = pygame.sprite.Group()

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

        # lava
        level_width = len(terrain_layout[0]) * tile_size + 200
        self.lava = Lava(screen_height - 135, level_width)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for column_index, val in enumerate(row):
                if val != '-1':
                    x = column_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = cutout_graphics('../Graphics/Terrain/Dark_lvl0.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    if type == 'coins':
                        sprite = Coin(tile_size, x, y, '../Graphics/Coins/Coins')

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for column_index, val in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.spawn_jump_particles, change_health, self.sound)
                    self.player.add(sprite)
                if val == '1':
                    sprite = AnimatedTile(160, x, y - 75, '../Graphics/Portal/smaller')
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def spawn_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def horizontal_collisions(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

    def vertical_collisions(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 3 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 3) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def is_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def land_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)

            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def check_coin_collected(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.coins += 1

    def check_death(self):
        if self.player.sprite.rect.top > screen_height or self.current_health <= 0:
            self.lives -= 1
            if self.lives == 0:
                self.hit_sound.play()
                end()
            else:
                self.hit_sound.play()
                respawn(Level(Level_0, screen, self.lives, self.coins, self.sound))

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            completed()

    def change_health(self, amount):
        self.current_health += amount

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -10
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    self.enemy_stomp.play()
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def run(self):

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # Lava
        self.lava.draw(self.display_surface, self.world_shift)

        # run the entire game / level
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        # check win or death
        self.check_death()
        self.check_win()

        # Check coin collisions
        self.check_coin_collected()

        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_collisions()
        self.is_player_on_ground()
        self.vertical_collisions()
        self.land_dust()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # Check enemy collisions
        self.check_enemy_collisions()
        # overlay
        self.overlay.show_health(self.current_health, self.max_health)
        self.overlay.show_coins(self.coins)

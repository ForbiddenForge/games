import sys
from os import walk
from random import randint

import pygame
from entity import Entity
from pygame.math import Vector2 as vector
from settings import PATHS


class Monster:
    def get_player_distance_direction(self):
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()

        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = vector()
        return (distance, direction)

    def face_player(self):
        distance, direction = self.get_player_distance_direction()
        if distance < self.notice_radius:
            if -0.5 < direction.y < 0.5:
                if direction.x < 0:  # player to the left (near)
                    self.status = "left_idle"
                elif direction.x > 0:  # player to the right (near)
                    self.status = "right_idle"
            else:
                if direction.y < 0:  # player towards the top (far)
                    self.status = "up_idle"
                elif direction.y > 0:  # player towards the bottom(far)
                    self.status = "down_idle"

    def walk_to_player(self):
        distance, direction = self.get_player_distance_direction()
        if self.attack_radius < distance < self.walk_radius:
            self.direction = direction
            self.status = self.status.split("_")[0]
        elif distance > self.walk_radius * 2:
            self.direction = vector()


class Kanye(pygame.sprite.Sprite):
    def __init__(self, pos, group, path, collision_sprites, player):
        super().__init__(group)
        self.import_assets(path)
        self.frame_index = 0
        self.status = "walk"
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # Float based movement
        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 500
        self.player = player
        self.notice_radius = 300
        self.walk_radius = 200
        self.attack_radius = 100
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height * 0.6)
        self.mask = pygame.mask.from_surface(self.image)

    def justice(self):
        distance = self.get_player_distance_direction()[0]
        self.kanye_sound_path = PATHS["Soundbites"][randint(0, 4)]
        self.rap_sound = pygame.mixer.Sound(self.kanye_sound_path)
        if distance < self.attack_radius:
            self.rap_sound.play().set_volume(0.8)

    def import_assets(self, path):
        self.animations = {}

        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                # sort the file names by number--0.png becomes just 0 and sort accordingly
                for file_name in sorted(
                    folder[2], key=lambda string: int(string.split(".")[0])
                ):
                    path = folder[0].replace("\\", "/") + "/" + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    surf = pygame.transform.scale(surf, (100, 100))
                    key = folder[0].split("\\")[1]
                    self.animations[key].append(surf)

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def get_player_distance_direction(self):
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()

        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = vector()
        return (distance, direction)

    def walk_to_player(self):
        distance, direction = self.get_player_distance_direction()
        if self.attack_radius < distance < self.walk_radius:
            self.direction = direction
        elif distance > self.walk_radius * 2:
            self.direction = vector()

    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        if self.direction.x != 0:
            direction = "horizontal"
        elif self.direction.y != 0:
            direction = "vertical"
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.walk_to_player()

        self.move(dt)
        self.animate(dt)


class Coffin(Entity, Monster):
    def __init__(self, pos, group, path, collision_sprites, player):
        super().__init__(pos, group, path, collision_sprites)

        # Overwrite dunder init attributes inherited from class Entity
        self.speed = 85

        # Player interaction
        self.player = player
        self.notice_radius = 600
        self.walk_radius = 500
        self.attack_radius = 50
        self.health = 1

    def attack(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0

        if self.attacking:
            self.status = self.status.split("_")[0] + "_attack"

    def animate(self, dt):
        current_animation = self.animations[self.status]
        if int(self.frame_index) == 4 and self.attacking:
            if self.get_player_distance_direction()[0] < self.attack_radius:
                self.player.damage()

        self.frame_index += 7 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False
        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.face_player()
        self.walk_to_player()
        self.attack()

        self.move(dt)
        self.animate(dt)
        self.blink()

        self.vulnerability_timer()
        self.check_health()


class Cactus(Entity, Monster):
    def __init__(self, pos, group, path, collision_sprites, player, create_bullet):
        super().__init__(pos, group, path, collision_sprites)
        self.player = player
        self.speed = 70
        self.notice_radius = 700
        self.walk_radius = 600
        self.attack_radius = 400
        self.create_bullet = create_bullet
        self.bullet_shot = False
        self.health = 1

    def attack(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0
            self.bullet_shot = False
        if self.attacking:
            self.status = self.status.split("_")[0] + "_attack"

    def animate(self, dt):
        current_animation = self.animations[self.status]

        if int(self.frame_index) == 6 and self.attacking and not self.bullet_shot:
            direction = self.get_player_distance_direction()[1]
            pos = self.rect.center + direction * 150
            self.create_bullet(pos, direction)
            self.bullet_shot = True

        self.frame_index += 7 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.face_player()
        self.walk_to_player()
        self.attack()

        self.move(dt)
        self.animate(dt)
        self.blink()

        self.vulnerability_timer()
        self.check_health()

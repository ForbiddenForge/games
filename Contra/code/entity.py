from math import sin
from os import walk

import pygame
from pygame.math import Vector2 as vector
from settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, path, group, shoot):
        super().__init__(group)
        
        # Graphics setup
        self.import_assets(path)
        self.frame_index = 0
        self.status = "right"
        
        # Images Setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = LAYERS["Level"]
        self.mask = pygame.mask.from_surface(self.image)
        
        # Float based movement
        self.direction = vector()
        self.pos = vector(self.rect.topleft)
        self.speed = 400
        
        # Interaction methods
        self.shoot = shoot

        # Bullet Timer
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown = 200
        self.duck = False
        
        self.health = 3
        self.is_vulnerable = True
        self.hit_time = 0
        self.invulnerable_duration = 1000
        
    def blink(self):
        if not self.is_vulnerable:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey(0,0)
                self.image = white_surf
    
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: 
            return True
        else:
            return False
        
    def damage(self):
        if self.is_vulnerable:
            self.health -= 1
            self.is_vulnerable = False
            self.hit_time = pygame.time.get_ticks()

            
        
    def check_death(self):
        if self.health <= 0:
            self.kill()
        
    def animate(self, dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

        
    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.cooldown:
                self.can_shoot = True
                
    def invulnerable_timer(self):
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > self.invulnerable_duration:
                self.is_vulnerable = True
        
        
    def import_assets(self, path):
        self.animations = {}

        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(
                    folder[2],
                    key=lambda file_name_string: int(file_name_string.split(".")[0]),
                ):
                    path = folder[0].replace("\\", "/") + "/" + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split("\\")[1]
                    self.animations[key].append(surf)
                    
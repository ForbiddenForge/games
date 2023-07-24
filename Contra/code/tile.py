import pygame
from pygame.math import Vector2 as vector
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, z):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


class CollisionTile(Tile):
    def __init__(self, pos, surf, group):
        super().__init__(pos, surf, group, LAYERS["Level"])
        self.old_rect = self.rect.copy()


class MovingPlatform(CollisionTile):
    def __init__(self, pos, surf, group):
        super().__init__(pos, surf, group)

        self.direction = vector(0, -1)
        self.speed = 200
        self.pos = vector(self.rect.topleft)

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

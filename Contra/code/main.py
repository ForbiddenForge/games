
import sys

import pygame
from player import Player
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from settings import *
from tile import CollisionTile, MovingPlatform, Tile
from bullet import Bullet


class Allsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("CONTRA STYLE GAMEEEE")
        self.clock = pygame.time.Clock()

        # groups['BG', 'BG Detail', 'FG Detail Bottom', 'FG Detail Top']

        self.all_sprites = Allsprites()
        self.collision_sprites = pygame.sprite.Group()
        self.platforms_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.setup()

        # Bullet images
        self.bullet_surf = pygame.image.load("../graphics/bullet.png").convert_alpha()

    def shoot(self, pos, direction, entity):
        Bullet(
            pos, self.bullet_surf, direction, [self.all_sprites, self.bullet_sprites]
        )

    def setup(self):

        tmx_map = load_pygame("../data/map.tmx")

        # Collision Tiles
        for x, y, surf in tmx_map.get_layer_by_name("Level").tiles():
            CollisionTile(
                pos=(x * 64, y * 64),
                surf=surf,
                group=[self.all_sprites, self.collision_sprites],
            )

        layer_list = ["BG", "BG Detail", "FG Detail Bottom", "FG Detail Top"]

        # Tiles
        for layer in layer_list:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile(
                    pos=(x * 64, y * 64),
                    surf=surf,
                    group=self.all_sprites,
                    z=LAYERS[layer],
                )

        # Objects
        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player(
                    (obj.x, obj.y),
                    self.all_sprites,
                    "../graphics/player",
                    self.collision_sprites,
                    self.shoot,
                )
        # type: ignore
        # Make an empty list for the border rectangles
        self.platform_border_rects = []
        for obj in tmx_map.get_layer_by_name("Platforms"):
            if obj.name == "Platform":
                MovingPlatform(
                    pos=(obj.x, obj.y),
                    surf=obj.image,
                    group=[
                        self.all_sprites,
                        self.collision_sprites,
                        self.platforms_sprites,
                    ],
                )
            else:
                border_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.platform_border_rects.append(border_rect)

    def platform_collisions(self):
        for platform in self.platforms_sprites.sprites():
            for border in self.platform_border_rects:
                if platform.rect.colliderect(border):
                    if platform.direction.y < 0:  # moving up
                        platform.rect.top = border.bottom
                        platform.pos.y = platform.rect.y
                        platform.direction.y = 1
                    else:  # down
                        platform.rect.bottom = border.top
                        platform.pos.y = platform.rect.y
                        platform.direction.y = -1
            if (
                platform.rect.colliderect(self.player.rect)
                and self.player.rect.centery > platform.rect.centery
            ):
                platform.rect.bottom = self.player.rect.top
                platform.pos.y = platform.rect.y
                platform.direction.y = -1

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.display_surface.fill((249, 131, 103))
            self.platform_collisions()
            self.all_sprites.update(dt)
            self.all_sprites.custom_draw(self.player)

            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.run()

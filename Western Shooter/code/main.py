import sys

import pygame
from monster import Cactus, Coffin, Kanye
from player import Player
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from settings import *
from sprite import Bullet, Sprite


class ALLSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load("../graphics/other/bg.png").convert()

    def customize_draw(self, player):
        # change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # blit the surfaces (bg, and sprites inside of group)
        self.display_surface.blit(self.bg, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("COWBOIIII")
        self.clock = pygame.time.Clock()
        self.bullet_surf = pygame.image.load(
            "../graphics/other/particle.png"
        ).convert_alpha()

        # Groups
        self.all_sprites = ALLSprites()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.setup()
        self.music = pygame.mixer.Sound("../sound/music.mp3")
        self.music.play(loops=-1).set_volume(0.2)
        self.bullet_sound = pygame.mixer.Sound("../sound/bullet.wav")
        self.hit_sound = pygame.mixer.Sound("../sound/hit.mp3")
        # self.bullet_sound.play().set_volume(0.2)

        self.rap_delay = 10000
        self.rap_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.rap_event, self.rap_delay)

    def display_score(self):
        font = pygame.font.Font(
            "../../asteroid_shooter_files/project_1 - blank window/graphics/subatomic.ttf",
            24,
        )
        score_text = f"Player Health: {self.player.health}"
        text_surf = font.render(score_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(topleft=(50, 50))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            self.display_surface,
            "white",
            text_rect.inflate(50, 50),
            width=5,
            border_radius=52,
        )

    def create_bullet(self, pos, direction):
        Bullet(pos, direction, self.bullet_surf, [self.all_sprites, self.bullets])
        self.bullet_sound.play().set_volume(0.2)

    def bullet_collision(self):
        # Bullet Obstacle Collisions
        for obstacle in self.obstacles.sprites():
            pygame.sprite.spritecollide(
                obstacle, self.bullets, True, pygame.sprite.collide_mask
            )
        # Bullet Monster Collisions
        for bullet in self.bullets.sprites():
            sprites = pygame.sprite.spritecollide(
                bullet, self.monsters, False, pygame.sprite.collide_mask
            )

            if sprites:
                bullet.kill()
                for sprite in sprites:
                    sprite.damage()
                    self.hit_sound.play().set_volume(0.2)

        # Player Bullet Collisions
        if pygame.sprite.spritecollide(
            self.player, self.bullets, True, pygame.sprite.collide_mask
        ):
            self.player.damage()
            self.hit_sound.play().set_volume(0.2)

    def setup(self):
        tmx_map = load_pygame("../data/map.tmx")
        # Import tiles, account for pixel size of each tile coordinate! (x64 in this instance)
        for x, y, surf in tmx_map.get_layer_by_name("Fence").tiles():
            Sprite((x * 64, y * 64), surf, [self.all_sprites, self.obstacles])

        # Import objects
        for obj in tmx_map.get_layer_by_name("Objects"):
            Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])

        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    path=PATHS["player"],
                    collision_sprites=self.obstacles,
                    create_bullet=self.create_bullet,
                )
            if obj.name == "Coffin":
                Coffin(
                    pos=(obj.x, obj.y),
                    group=[self.all_sprites, self.monsters],
                    path=PATHS["coffin"],
                    collision_sprites=self.obstacles,
                    player=self.player,
                )
            if obj.name == "Cactus":
                Cactus(
                    pos=(obj.x, obj.y),
                    group=[self.all_sprites, self.monsters],
                    path=PATHS["cactus"],
                    collision_sprites=self.obstacles,
                    player=self.player,
                    create_bullet=self.create_bullet,
                )
            if obj.name == "Kanye":
                self.kanye = Kanye(
                    pos=(obj.x, obj.y),
                    group=[self.all_sprites],
                    path=PATHS["Kanye"],
                    collision_sprites=self.obstacles,
                    player=self.player,
                )

    def run(self):
        while True:
            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == self.rap_event:
                    self.kanye.justice()

            dt = self.clock.tick() / 1000

            # Update Groups
            self.all_sprites.update(dt)
            self.bullet_collision()
            # Draw Groups
            self.display_surface.fill(("black"))
            self.all_sprites.customize_draw(self.player)
            self.display_score()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

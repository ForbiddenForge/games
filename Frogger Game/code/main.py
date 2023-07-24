import sys
from random import choice, randint, uniform

import pygame
from car import Car
from player import Player
from settings import *
from sprite import *

print("frogger game yeah")


class AllSprites(pygame.sprite.Group):
    def __init__(self):

        super().__init__()

        self.offset = pygame.math.Vector2()

        self.bg = pygame.image.load("../graphics/main/map.png").convert()
        self.fg = pygame.image.load("../graphics/main/overlay.png").convert_alpha()

    def customize_draw(self):
        # Change the Offset Vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH // 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT // 2

        # Blit the background
        display_surface.blit(self.bg, -self.offset)

        # We use sorted for the list of sprites by y value to indicate draw order (3D effects)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            # blit anything in place of existing sprites to be drawn
            # size = sprite.rect.size
            # surf = pygame.Surface(size)
            # surf.fill('green')

            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, offset_pos)

        display_surface.blit(self.fg, -self.offset)


# Basic Setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, +WINDOW_HEIGHT))
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()

# Groups
all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# Sprites
player = Player(
    position=(2062, 3274), group=all_sprites, collision_sprites=obstacle_sprites
)
pos_list = []

# Font
font = pygame.font.Font(None, 50)
text_surface = font.render("You Won!!!! :)", True, (200, 190, 155))
text_rect = text_surface.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# Music

game_music = pygame.mixer.Sound("../audio/music.mp3")
game_music.play(loops=-1).set_volume(0.20)

# Timers

car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 50)

# Sprite Setup
for file_name, pos_list in SIMPLE_OBJECTS.items():
    path = f"../graphics/objects/simple/{file_name}.png"
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        SimpleSprite(surf, pos, [all_sprites, obstacle_sprites])

for file_name, pos_list in LONG_OBJECTS.items():
    path = f"../graphics/objects/long/{file_name}.png"
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        LongSprite(surf, pos, [all_sprites, obstacle_sprites])

# Game Loop
while True:

    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == car_timer:
            random_pos = choice(CAR_START_POSITIONS)
            if random_pos not in pos_list:
                pos_list.append(random_pos)
                pos = (random_pos[0], random_pos[1] + randint(-8, 8))
                Car(position=pos, group=[all_sprites, obstacle_sprites])
            if len(pos_list) > 5:
                del pos_list[0]

    # Delta Time
    dt = clock.tick() / 1000

    # Draw Background
    display_surface.fill((190, 26, 99))

    if player.pos.y > 1180:
        # Update Groups
        all_sprites.update(dt)
        # Drawing
        # all_sprites.draw(display_surface)
        all_sprites.customize_draw()
    else:
        display_surface.fill((56, 76, 99))
        display_surface.blit(text_surface, text_rect)
        pygame.draw.rect(
            display_surface,
            (200, 190, 155),
            text_rect.inflate(50, 60),
            width=12,
            border_radius=50,
        )
    # Update Display Surface
    pygame.display.update()

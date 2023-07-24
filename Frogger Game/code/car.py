import pygame
from os import walk
from random import choice


class Car(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.name = "car"

        # Get a random car file name i.e. 'green.png'
        for folder_name, sub_folders, file_list in walk("../graphics/cars"):
            car_name = choice(file_list)

        self.image = pygame.image.load("../graphics/cars/" + car_name).convert_alpha()
        self.rect = self.image.get_rect(center=position)

        # Float based movement
        self.position = pygame.math.Vector2(self.rect.center)

        if position[0] < 200:
            self.direction = pygame.math.Vector2(1, 0)
        else:
            self.direction = pygame.math.Vector2(-1, 0)
            self.image = pygame.transform.flip(self.image, True, False)

        self.speed = 300
        self.hitbox = self.rect.inflate(0, -self.rect.height  / 2)

    def update(self, dt):
        self.position += self.direction * self.speed * dt
        self.hitbox.center = (round(self.position.x), round(self.position.y))
        self.rect.center = self.hitbox.center

        if not -200 < self.rect.x < 3400:
            self.kill()

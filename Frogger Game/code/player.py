import pygame, sys
from settings import *
from os import walk

class Player(pygame.sprite.Sprite):

	def __init__(self, position, group, collision_sprites):
		super().__init__(group)

		#image
		self.import_assets()
		self.frame_index = 0
		self.status = 'down'
		# self.image = self.animation[self.frame_index]
		self.image = self.animations_dict[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = position)
		self.mask = pygame.mask.from_surface(self.image)

		# Float based movement
		self.pos = pygame.math.Vector2(self.rect.center)
		self.direction = pygame.math.Vector2()
		self.speed = 200

		#collisions
		self.collision_sprites = collision_sprites
		self.hitbox = self.rect.inflate(0, -self.rect.height / 2)

	def collision(self, direction):
		if direction == 'horizontal':
			for sprite in self.collision_sprites.sprites():
				if sprite.hitbox.colliderect(self.hitbox):
					if hasattr(sprite, 'name') and sprite.name == 'car':
						pygame.quit()
						sys.exit()

					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right
						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx

		else:
			for sprite in self.collision_sprites.sprites():
				if sprite.hitbox.colliderect(self.hitbox):
					if hasattr(sprite, 'name') and sprite.name == 'car':
						pygame.quit()
						sys.exit()

					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery
			#vertical collisions



	def import_assets(self):
		self.animations_dict = {}
		for index, folder in enumerate(walk('../graphics/player')):
			if index == 0:
				for name in folder[1]:
					self.animations_dict[name] = []
			else:
				for file_name in folder[2]:
					path = folder[0].replace('\\', '/') + '/' + file_name
					surf = pygame.image.load(path).convert_alpha()
					key = folder[0].split('\\')[1]
					self.animations_dict[key].append(surf)

		# self.file_name_directions = ['down', 'left', 'right', 'up']
		# self.file_name_list = [[f'../graphics/player/{direction}/{number}.png' for number in range(1,5)]
		# for direction in self.file_name_directions]
		# for filename in self.animation:
		# 	print( filename)

	def input(self):
		keys = pygame.key.get_pressed()
		# Horizontal Input
		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.status = 'right'
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.status = 'left'
		else:
			self.direction.x = 0 

		# Vertical Input
		if keys[pygame.K_UP]:
			self.direction.y = -1
			self.status = 'up'
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
			self.status = 'down'
		else:
			self.direction.y = 0
		
	def move(self,dt):
		# normalize a vector -> length of a vector should be 1
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		# Horizontal movement + collision
		self.pos.x += self.direction.x * self.speed * dt 
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')

		# Vertical movement + collision
		self.pos.y += self.direction.y * self.speed * dt 
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')


	def animate(self,dt):
		current_animation = self.animations_dict[self.status]

		if self.direction.magnitude() != 0:
			self.frame_index += 10 * dt 
			if self.frame_index >= len(current_animation):
				self.frame_index = 0
		else:
			self.frame_index = 0
		self.image = current_animation[int(self.frame_index)]

	def restrict(self):
		if self.rect.left < 640:
			self.pos.x = 640 + self.rect.width / 2
			self.hitbox.left = 640
			self.rect.left = 640
		if self.rect.right > 2560:
			self.pos.x = 2560 - self.rect.width / 2
			self.hitbox.right = 2560
			self.rect.right = 2560
		if self.rect.bottom > 3500:
			self.pos.y = 3500 - self.rect.height / 2
			self.hitbox.centery = self.rect.centery
			self.rect.bottom = 3500

	def update(self,dt):
		self.input()
		self.move(dt)
		self.animate(dt)
		self.restrict()





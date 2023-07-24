import pygame


class Overlay:
    def __init__(self,player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.health_surf = pygame.image.load('../graphics/health.png').convert_alpha()
        
    def display(self):
        # blit the health bar surface * player health number
        
        for health_bar in range(self.player.health):
            x_pos = 10 + health_bar * (self.health_surf.get_width() + 3)
            y_pos = 10
            self.display_surface.blit(self.health_surf, (x_pos, y_pos))
        
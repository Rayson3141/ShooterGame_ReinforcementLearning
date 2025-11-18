import pygame
from pygame.sprite import Sprite

class Target(Sprite):
    """Class for Target ships"""

    def __init__(self, sg_game):
        # Defining the location
        super().__init__()
        self.window = sg_game.window
        self.settings = sg_game.set
        self.image = pygame.image.load('images/target.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self):
        window_rect = self.window.get_rect()
        if self.rect.right >= window_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.settings.target_speed * self.settings.fleet_direction)
        self.rect.x = self.x
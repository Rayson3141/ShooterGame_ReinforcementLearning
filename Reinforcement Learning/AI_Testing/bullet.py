import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class for the bullet used in the Shooter Game"""

    def __init__(self,sg_game):
        """Create a bullet object"""
        super().__init__()
        self.window = sg_game.window
        self.set = sg_game.set
        self.colour = self.set.bullet_colour

        # Creating a bullet
        self.rect = pygame.Rect(0,0,self.set.bullet_width, self.set.bullet_height)
        # Moving the bullet to the correct position
        self.rect.midtop = sg_game.shooter.rect.midtop

        # Store the exact position of the bullet
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up"""
        self.y -= self.set.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet on screen"""
        pygame.draw.rect(self.window, self.colour, self.rect)
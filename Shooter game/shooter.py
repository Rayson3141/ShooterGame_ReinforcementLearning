import pygame
from pygame.sprite import Sprite

class Shooter(Sprite):
    """A class to manage the shooter"""

    def __init__(self, sg_game):
        """Initialize the shooter and set its starting position"""
        super().__init__()
        self.window = sg_game.window
        self.window_rect = sg_game.window.get_rect()
        self.set = sg_game.set

        # Load the shooter picture and get its rect.
        self.pic = pygame.image.load('images/shooter.bmp')
        self.rect = self.pic.get_rect()

        # Rule of sprite group need the name "image".
        self.image = self.pic

        # Start each new shooter at the bottom center of the screen"""
        self.rect.midbottom = self.window_rect.midbottom

        # Movement flag; start with not moving
        self.move_left = False
        self.move_right = False

        # Store the exact horizontal coordiante of the shooter
        self.x = float(self.rect.x)

    def update(self):
        """Update the shooter position based on movement flag."""
        if self.move_right and self.rect.right < self.window_rect.right:
            self.x += self.set.shooter_speed
        if self.move_left and self.rect.left > 0:
            self.x -= self.set.shooter_speed
        self.rect.x = self.x

    def draw_shooter(self):
        """Draw the shooter"""
        self.window.blit(self.pic, self.rect)

    def center_shooter(self):
        """Center the chooter on the screen"""
        self.rect.midbottom = self.window_rect.midbottom
        self.x = float(self.rect.x)
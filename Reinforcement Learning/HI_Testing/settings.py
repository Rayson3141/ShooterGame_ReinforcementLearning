import pygame


########################################################################

class Settings:
    """Class for game settings"""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen set
        self.window_width = 1200
        self.window_height = 800
        self.bg_colour = (230, 230, 230)
        self.shooter_limit = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)
        self.fleet_drop_speed = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the target point values increase
        self.result_scale = 1.5

        self.initialize_dynamic_set()

        """Difficulty change"""
        # self.speedup_scale = 1.5
        # self.result_scale = 1.5
        self.initialize_dynamic_set()

    def initialize_dynamic_set(self):
        """Initialize settings that change throughout the game."""
        self.shooter_speed = 1.5*40
        self.bullet_speed = 2.5*40
        self.target_speed = 1.0*40
        self.anothership_speed = 1.5

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.max_bullet_no = 3

        # Scoring set
        self.target_points = 50

    def increase_speed(self):
        """Increase speed settings and target point values."""
        self.shooter_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.target_speed *= self.speedup_scale
        self.target_points = int(self.target_points * self.result_scale)



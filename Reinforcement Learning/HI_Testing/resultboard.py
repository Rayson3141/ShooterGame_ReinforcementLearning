import pygame.font
from pygame.sprite import Group

from shooter import Shooter

class Resultboard:
    """A class to report result"""

    def __init__(self, sg_game):
        """Initialize resultkeeping attributes."""
        self.sg_game = sg_game
        self.window = sg_game.window
        self.window_rect = self.window.get_rect()
        self.set = sg_game.set
        self.stats = sg_game.stats
        
        # Font set for result.
        self.text_colour = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Ready the initial result picture.
        self.ready_result()
        self.ready_best_result()
        self.ready_level()
        self.ready_shooters()

    def ready_result(self):
        """Turn the result into a rendered picture."""
        rounded_result = round(self.stats.result, -1)
        result_str = f"{rounded_result:,}"
        self.result_pic = self.font.render(result_str, True,
                self.text_colour, self.set.bg_colour)

        # Display the result at the top right of the screen.
        self.result_rect = self.result_pic.get_rect()
        self.result_rect.right = self.window_rect.right - 20
        self.result_rect.top = 20

    def show_result(self):
        """Draw result, level and target to the window."""
        self.window.blit(self.result_pic, self.result_rect)
        self.window.blit(self.best_result_pic, self.best_result_rect)
        self.window.blit(self.level_pic, self.level_rect)
        self.shooter.draw(self.window)

    def ready_best_result(self):
        """Turn the best result into a rendered picture."""
        best_result = round(self.stats.best_result, -1)
        best_result_str = f"{best_result:,}"
        self.best_result_pic = self.font.render(best_result_str, True,
                 self.text_colour, self.set.bg_colour)

        # Center the best result at the top of the window.
        self.best_result_rect = self.best_result_pic.get_rect()
        self.best_result_rect.centerx = self.window_rect.centerx
        self.best_result_rect.top = self.result_rect.top

    def check_best_result(self):
        """Check to see if there's a new best result."""
        if self.stats.result > self.stats.best_result:
            self.stats.best_result = self.stats.result
            self.ready_best_result()

    def ready_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_pic =self.font.render(level_str, True,
                self.text_colour, self.set.bg_colour)

        # Position the level below the score.
        self.level_rect = self.level_pic.get_rect()
        self.level_rect.right = self.result_rect.right
        self.level_rect.top = self.result_rect.bottom + 10

    def ready_shooters(self):
        """Show how many shooters are left."""
        self.shooter = Group()
        for num_shooter in range(self.stats.shooters_left):
            shooter = Shooter(self.sg_game)
            shooter.rect.x = 10 + num_shooter * shooter.rect.width
            shooter.rect.y = 10
            self.shooter.add(shooter)

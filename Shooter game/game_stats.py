class GameStats:
    """Game data monitoring"""

    def __init__(self, sg_game):
        """Data initialization"""
        self.settings = sg_game.set
        self.reset_stats()
        self.game_active = False
        self.best_result = 0

    def reset_stats(self):
        self.shooters_left = self.settings.shooter_limit
        self.result = 0
        self.level = 1
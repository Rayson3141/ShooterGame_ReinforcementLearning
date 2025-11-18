import pygame.font

class Button:
    """A class to build buttons for the game."""

    def __init__(self, sg_game, message):
        """Initialize button attributes."""
        self.window = sg_game.window
        self.window_rect = self.window.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_colour = (0,135,0)
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.window_rect.center

        # The button message needs to be ready only once.
        self._ready_message(message)

    def _ready_message(self, message):
        """Turn message into a rendered image and center text on the button."""
        self.message_pic = self.font.render(message, True, self.text_colour, self.button_colour)
        self.message_pic_rect = self.message_pic.get_rect()
        self.message_pic_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.window.fill(self.button_colour, self.rect)
        self.window.blit(self.message_pic, self.message_pic_rect)

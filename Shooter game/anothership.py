import pygame

class AnotherShip:
    def __init__(self,ai_game):
        self.screen = ai_game.window
        self.settings = ai_game.set
        self.screen_rect = ai_game.window.get_rect()

        self.image = pygame.image.load('images/小黑子.bmp')
        self.rect = self.image.get_rect()

        self.rect.bottomleft = self.screen_rect.bottomleft
        self.rect.y -= self.rect.height
        self.x = float(self.rect.x)
        self.moving_right = True
        self.moving_left = False

    def updateanothership(self):
        if self.moving_right:
            self.x += self.settings.anothership_speed
            self.rect.x = self.x
        elif self.moving_left:
            self.x -= self.settings.anothership_speed
            self.rect.x = self.x
        if self.rect.x == 0:
            self.moving_right = True
            self.moving_left = False
        elif self.rect.right == self.screen_rect.right:
            self.moving_right = False
            self.moving_left = True


    def blitme(self):
        self.screen.blit(self.image,self.rect)


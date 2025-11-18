import random
import sys
import pygame
import numpy as np

from time import sleep

from settings import Settings
from shooter import Shooter
from bullet import Bullet
from target import Target
from game_stats import GameStats
from resultboard import Resultboard
from button import Button
from anothership import AnotherShip
from anotherbullet import Anotherbullet


class ShooterGame:
    """A Shooter Game"""

    def __init__(self, agent):
        """Initialize the game and create game resource"""
        pygame.init()
        pygame.mixer.init()
        self.agent = agent

        self.fps = pygame.time.Clock()
        self.tick = 0
        self.set = Settings()
        self.window = pygame.display.set_mode((self.set.window_width, self.set.window_height))
        pygame.display.set_caption("Shooter Game")

        # Create an instance to store game statistics,
        # Create a resultboard.
        self.stats = GameStats(self)
        self.sb = Resultboard(self)
        self.shooter = Shooter(self)
        self.target = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.ai_bullets = pygame.sprite.Group()
        self._create_fleet()
        self.ai_shooter = AnotherShip(self)

        # Start Shooter Game in an inactive state.
        self.stats.game_active = False

        # Make the play button
        self.play_button = Button(self, "Play")

    def playmusic(self, m):
        audio = ['start.mp3', 'fire.mp3']

        pygame.mixer.music.load(audio[m])
        pygame.mixer.music.play(0)

    def run(self):
        self.playmusic(0)
        """Run the game"""
        state = [500, 500]
        target_y = 500
        target_speed = self.set.target_speed
        speed = target_speed * self.set.fleet_direction

        while True:
            self._inputs_check()
            if self.stats.game_active:
                action = self.agent.act(state, target_y, speed)
                self._inputs_check1(action)
                self.shooter.update()
                self._bullets_update()
                self._target_update()
                self.ai_shooter.updateanothership()
                self._ai_fire()

                target_kill = max(self.target.sprites(), key=lambda sprite: sprite.rect.y)
                next_state = (target_kill.rect.centerx, self.shooter.x)
                state = next_state
                target_y = target_kill.rect.y
                target_speed = self.set.target_speed
                speed = target_speed * self.set.fleet_direction
            self._draw_new_window()
            self.shooter.move_right = False
            self.shooter.move_left = False
            self.fps.tick(60)

    def _inputs_check(self):
        """Responds to mouse and keyboard input."""
        for input in pygame.event.get():
            if input.type == pygame.QUIT:
                sys.exit()
            elif input.type == pygame.MOUSEBUTTONDOWN:
                mouse_loc = pygame.mouse.get_pos()
                self._check_play_button(mouse_loc)

    def _inputs_check1(self, action):
        if action == 1:
            self.shooter.move_right = True
        elif action == 2:
            self.shooter.move_left = True
        elif action == 0:
            self._shoot_bullet()

    def _shoot_bullet(self):
        """Create a new bullet and add it to the bullet group"""
        if len(self.bullets) < self.set.max_bullet_no:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.playmusic(1)

    def _bullets_update(self):
        """Update position of bullets and get rid of out of window bullets."""

        # Update bullet position
        self.bullets.update()
        self.ai_bullets.update()

        # Getting rid of out of window bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        for ai_bullet in self.ai_bullets.copy():
            if ai_bullet.rect.bottom <= 0:
                self.ai_bullets.remove(ai_bullet)

        self._check_bullet_target_collision()

    def _check_fleet_edges(self):
        for target in self.target.sprites():
            if target.check_edges():
                self._change_fleet_direction()
                break

    def _create_fleet(self):
        """Create target fleet"""
        target = Target(self)
        target_width, target_height = target.rect.size
        available_space_x = self.set.window_width - (2 * target_width)
        number_target_x = available_space_x // (2 * target_width)

        """Determining the number of row"""
        shooter_height = self.shooter.rect.height
        available_space_y = (self.set.window_height -
                             (2 * target_height) - shooter_height)
        number_rows = available_space_y // (2 * target_height)

        for row_number in range(number_rows):
            for target_number in range(number_target_x):
                self._create_target(target_number, row_number)

    def _create_target(self, target_number, row_number):
        target = Target(self)
        target_width, target_height = target.rect.size
        target.x = target_width + 2 * target_width * target_number
        target.rect.x = target.x
        target.rect.y = target.rect.height + 2 * target.rect.height * row_number
        self.target.add(target)

    def _change_fleet_direction(self):
        for target in self.target.sprites():
            target.rect.y += self.set.fleet_drop_speed
        self.set.fleet_direction *= -1

    def _ai_fire(self):
        """Create a bullet for the ai shooter"""
        if self.tick < 60:
            self.tick += 1
        else:
            self.tick = 0
        ramdom = random.randint(1, 59)
        if self.tick == ramdom:
            new_ai_bullet = Anotherbullet(self)
            self.ai_bullets.add(new_ai_bullet)

    def _check_play_button(self, mouse_pos):
        """Starting game"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.ready_result()
            self.sb.ready_level()
            self.sb.ready_shooters()
            self.target.empty()
            self.bullets.empty()
            self._create_fleet()
            self.shooter.center_shooter()
            pygame.mouse.set_visible(False)
            self.set.initialize_dynamic_set()
            self.tick = 0

    def _shooter_hit(self):
        if self.stats.shooters_left > 0:
            self.stats.shooters_left -= 1
            self.sb.ready_shooters()
            self.target.empty()
            self.bullets.empty()
            self._create_fleet()
            self.shooter.center_shooter()
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_target_bottom(self):
        """Checking the shooter's arrival to the end"""
        window_rect = self.window.get_rect()
        for target in self.target.sprites():
            if target.rect.bottom >= window_rect.bottom:
                self._shooter_hit()
                break

    def _check_bullet_target_collision(self):
        """Bullet hit check"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.target, True, True)
        if collisions:
            for target in collisions.values():
                self.stats.result += self.set.target_points * len(target)
            self.sb.ready_result()
            self.sb.check_best_result()

        pygame.sprite.groupcollide(self.ai_bullets, self.target, True, True)

        # Destroying existing bullets and create new fleet.
        if not self.target:
            self.bullets.empty()
            self.ai_bullets.empty()
            self._create_fleet()
            self.set.increase_speed()
            self.stats.level += 1
            self.sb.ready_level()

    def _target_update(self):
        self._check_fleet_edges()
        self.target.update()
        """Player collision with target"""
        if pygame.sprite.spritecollideany(self.shooter, self.target):
            self._shooter_hit()
        self._check_target_bottom()

    def _draw_new_window(self):
        """Refreshing the window"""
        self.window.fill(self.set.bg_colour)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for ai_bullet in self.ai_bullets.sprites():
            ai_bullet.draw_bullet()
        self.shooter.draw_shooter()
        self.ai_shooter.blitme()
        self.target.draw(self.window)
        self.sb.show_result()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    sg = ShooterGame()
    sg.run()
    pygame.mixer.music.play(1)

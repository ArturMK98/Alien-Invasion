import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button


class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Play the game in fullscreen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game stats and create a scoreboard
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        # Create a ship, a group of bullets, and a group of aliens
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Start Alien Invasion in an inactive state
        self.game_active = False
        self.waiting_for_difficulty = False
        self.game_over = False

        # Make the play button
        self.play_button = Button(self, "Play")

        # Make the restart button
        self.restart_button = Button(self, "Restart")

        # Make the quit button
        self.quit_button = Button(self, "Quit", y_offset=80)

        

        # Make difficulty level buttons
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium", y_offset=80)
        self.hard_button = Button(self, "Hard", y_offset=160)

        # Prepare the 'Difficulty' text
        self._prep_difficulty_text()

        # Game over message
        self._prep_game_over_message()

    
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(100)


    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.game_active and not self.waiting_for_difficulty and not self.game_over:
                    self._check_play_button(mouse_pos)
                elif self.waiting_for_difficulty:
                    self._check_difficulty_buttons(mouse_pos)
                elif self.game_over:
                    self._check_restart_button(mouse_pos)
                    self._check_quit_button(mouse_pos)

    
    def _check_play_button(self,mouse_pos=None, p_pressed=False):
        """Start a new game when the player clicks play"""
        play_button_clicked = False
        if mouse_pos is not None:
            play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if play_button_clicked or p_pressed:
                self.waiting_for_difficulty = True
                

    def _check_restart_button(self, mouse_pos):
        """Restart the game when the player clicks restart"""
        restart_button_clicked = self.restart_button.rect.collidepoint(
                                                                    mouse_pos)
        if restart_button_clicked:
            self._restart_game()

    
    def _check_quit_button(self, mouse_pos):
        """Quit the game when the player clicks quit"""
        quit_button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if quit_button_clicked:
            sys.exit()


    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT and self.game_active:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT and self.game_active:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p and not self.game_active:
            self._check_play_button(p_pressed=True)
        elif event.key == pygame.K_r and self.game_over:
            self._restart_game()


    def _restart_game(self):
        """Restart the game"""
        self.game_over = False
        self.waiting_for_difficulty = True
        pygame.mouse.set_visible(True)
        

    def _check_difficulty_buttons(self, mouse_pos):
        """Check if the player has selected a difficulty"""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked:
            self.settings.set_easy_mode()
            self._start_game()
        elif medium_button_clicked:
            self.settings.set_medium_mode()
            self._start_game()
        elif hard_button_clicked:
            self.settings.set_hard_mode()
            self._start_game()


    def _start_game(self):
        """Initialize and start a new game session"""
        # Reset the game statistics
        #self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.scoreboard.prep_score()
        self.scoreboard.prep_high_score()
        self.scoreboard.prep_ships()
        self.scoreboard.prep_level()
        self.game_active = True
        self.waiting_for_difficulty = False
        self._reset_level()

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

    
    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullet positions
        self.bullets.update()
        
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collision()
    

    def  _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions"""
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_values()

            # Increase level
            self.stats.level += 1
            self.scoreboard.prep_level()


    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Same as if the ship got hit
                self._ship_hit()
                break


    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships left and update scoreboard
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            self._reset_level()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            self.game_over = True
            pygame.mouse.set_visible(True)

    
    def _reset_level(self):
        """Clear existing bullets/aliens, reset the fleet and center the ship"""
        # Get rid of any remaining bullets and aliens
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet and center ship
        self._create_fleet()
        self.ship.center_ship()


    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _create_fleet(self):
        """Create a fleet of aliens"""
        # Create an alien and keep adding until no space left
        # Spacing between aliens is 1 alien width and 1 alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 6 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished row; reset x value, and increment y value
            current_x = alien_width
            current_y += 2 * alien_height
    

    def _prep_difficulty_text(self):
        """Prepare the 'Difficulty' text"""
        self.difficulty_font = pygame.font.SysFont('Comic Sans MS', 48)
        self.difficulty_image = self.difficulty_font.render("Difficulty", 
                                                            True, (0, 0, 0))
        self.difficulty_rect = self.difficulty_image.get_rect()
        self.difficulty_rect.centerx = self.screen.get_rect().centerx
        self.difficulty_rect.top = self.easy_button.rect.top - 80  


    def _prep_game_over_message(self):
        """Prepare the 'Game Over' message"""
        self.game_over_font = pygame.font.SysFont('Comic Sans MS', 60)
        self.game_over_image = self.game_over_font.render("Game Over", 
                                                          True, (255, 0, 0))
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.center = self.screen.get_rect().center
        self.game_over_rect.y -= 100

    
    def _draw_difficulty_text(self):
        """Draw the 'Difficulty' text to the screen"""
        self.screen.blit(self.difficulty_image, self.difficulty_rect)


    def _draw_game_over_message(self):
        """Draw the 'Game Over' message to the screen"""
        self.screen.blit(self.game_over_image, self.game_over_rect)


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _update_screen(self):
        """Update the images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_colour)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw score information
        self.scoreboard.show_game_info()

        # Draw play button if game is inactive and not waiting for difficulty
        if not self.game_active and not self.waiting_for_difficulty and not self.game_over:
            self.play_button.draw_button()

        # Draw difficulty level buttons if waiting for difficulty
        if self.waiting_for_difficulty:
            self._draw_difficulty_text()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()

        if self.game_over:
            self._draw_game_over_message()
            self.restart_button.draw_button()
            self.quit_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
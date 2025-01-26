import sys
import pygame
from random import random
from random import randint
from random import choice
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien_bullet import AlienBullet
from alien import Alien
from death_effect import DeathEffect
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

        # Load the background image
        self.bg_image = pygame.image.load('assets/background.bmp')
        self.bg_image = pygame.transform.scale(
            self.bg_image, (
                self.settings.screen_width, self.settings.screen_height))
        
        # Load logo image
        self.logo_image = pygame.image.load('assets/alien_invasion.bmp')
        self.logo_image = pygame.transform.scale(self.logo_image, (600, 300))
        self.logo_rect = self.logo_image.get_rect()
        self.logo_rect.centerx = self.screen.get_rect().centerx
        self.logo_rect.top = 50
        
        # Load sound effects
        self.ship_shoot_sound = pygame.mixer.Sound('sound_effects/shot.mp3')
        self.alien_death_sound = pygame.mixer.Sound('sound_effects/sparkles.mp3')
        self.player_death_sound = pygame.mixer.Sound('sound_effects/explosion.mp3')
        self.alien_shoot_sounds = [
            pygame.mixer.Sound('sound_effects/fireball_whoosh_1.mp3'),
            pygame.mixer.Sound('sound_effects/fireball_whoosh_2.mp3')
        ]

        # Create an instance to store game stats and create a scoreboard
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        # Create a ship, a group of bullets, and a group of aliens
        self.ship = Ship(self, 'assets/player_ship.png', 3)
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.death_effects = pygame.sprite.Group()
        self._create_fleet()

        # Load custom font
        self.font = pygame.font.Font('assets/ThaleahFat.ttf', 48)
        self.small_font = pygame.font.Font('assets/ThaleahFat.ttf', 34)


        # Start Alien Invasion in an inactive state
        self.game_active = False
        self.waiting_for_difficulty = False
        self.game_over = False
        self.paused = False
        self.how_to_play_screen = False

        # Main menu buttons
        self.play_button = Button(self, "Play")
        self.how_to_play_button = Button(self, "How to Play", y_offset=80)
        self.settings_button_main = Button(self, "Settings", y_offset=160)
        self.quit_button_main = Button(self, "Quit", y_offset=240)

        # How to Play screen buttons
        self.back_button = Button(self, "Back", y_offset=240)

        # Make the restart button
        self.restart_button = Button(self, "Restart")

        # Make the quit button
        self.quit_button = Button(self, "Quit", y_offset=80)

        # Make difficulty level buttons
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium", y_offset=80)
        self.hard_button = Button(self, "Hard", y_offset=160)

        # Pause menu buttons
        self.resume_button = Button(self, "Resume", y_offset=-80)
        self.settings_button = Button(self, "Settings", y_offset=0)
        self.main_menu_button = Button(self, "Main Menu", y_offset=80)

        # Prepare the 'Difficulty' text
        self._prep_difficulty_text()

        # Game over message
        self._prep_game_over_message()

    
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.game_active and not self.paused:
                self.ship.update()
                self._update_bullets()
                self._update_alien_bullets()
                if not self.game_over:
                    self._update_aliens()
                self.death_effects.update()

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
                if not self.game_active and not self.waiting_for_difficulty and not self.game_over and not self.how_to_play_screen:
                    self._check_main_menu_buttons(mouse_pos)
                elif self.waiting_for_difficulty:
                    self._check_difficulty_buttons(mouse_pos)
                elif self.game_over:
                    self._check_restart_button(mouse_pos)
                    self._check_quit_button(mouse_pos)
                elif self.paused:
                    self._check_pause_menu_buttons(mouse_pos)
                elif self.how_to_play_screen:
                    self._check_how_to_play_buttons(mouse_pos)


    def _check_main_menu_buttons(self, mouse_pos):
        """Check which main menu button was clicked"""
        if self.play_button.rect.collidepoint(mouse_pos):
            self.waiting_for_difficulty = True
        elif self.how_to_play_button.rect.collidepoint(mouse_pos):
            self.how_to_play_screen = True
            pass
        elif self.settings_button_main.rect.collidepoint(mouse_pos):
            # Handle settings button click
            pass
        elif self.quit_button_main.rect.collidepoint(mouse_pos):
            sys.exit()


    def _check_how_to_play_buttons(self, mouse_pos):
        """Check which button was clicked on the 'How to Play' screen"""
        if self.back_button.rect.collidepoint(mouse_pos):
            self.how_to_play_screen = False


    def _check_pause_menu_buttons(self, mouse_pos):
        """Check which pause menu button was clicked"""
        if self.resume_button.rect.collidepoint(mouse_pos):
            self.paused = False
            pygame.mouse.set_visible(False)
        elif self.settings_button.rect.collidepoint(mouse_pos):
            # Handle settings button click
            pass
        elif self.main_menu_button.rect.collidepoint(mouse_pos):
            self._return_to_main_menu()

    
    def _return_to_main_menu(self):
        """Return to the main menu and reset the game state"""
        self.game_active = False
        self.paused = False
        self.waiting_for_difficulty = False
        self.game_over = False
        pygame.mouse.set_visible(True)
        self.stats.reset_stats()
        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()
        self.bullets.empty()
        self.aliens.empty()
        self.alien_bullets.empty()
        self.death_effects.empty()
        self.ship.center_ship()

    
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
        elif event.key == pygame.K_ESCAPE and self.game_active:
            self.paused = not self.paused
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
            new_bullet = Bullet(self, 'assets/bullet_player.png', 4)
            self.bullets.add(new_bullet)
            self.ship_shoot_sound.play()

    
    def _fire_alien_bullet(self, alien):
        """Fire a bullet from an alien"""
        # Allow only one alien to shoot at a time
        if len(self.alien_bullets) < 1:
            new_bullet = AlienBullet(self, alien, 'assets/bullet_alien.png', 4) 
            self.alien_bullets.add(new_bullet)
            choice(self.alien_shoot_sounds).play()


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
            self.bullets, self.aliens, 
            True, True,collided=self._hitbox_collision)
        
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    death_effect = DeathEffect(self, 
                                               alien.rect.center, 
                                               'assets/sparkle.png', 4, 
                                               self.settings.alien_width, 
                                               self.settings.alien_height)
                    self.death_effects.add(death_effect)
                    self.alien_death_sound.play()
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
            if self.settings.alien_width > 40 and self.settings.alien_height > 40:
                self.settings.alien_width -= 5
                self.settings.alien_height -= 5
            self.scoreboard.prep_level()


    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self._check_fleet_edges()
        self.aliens.update()

        # Check if any aliens can fire a bullet
        shooting_aliens = [
            alien for alien in self.aliens.sprites() if alien.can_shoot(self.aliens)]
        if shooting_aliens and random() < self.settings.alien_shoot_frequency:
            shooting_alien = choice(shooting_aliens)
            self._fire_alien_bullet(shooting_alien)

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(
            self.ship, self.aliens, collided=self._hitbox_collision):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    
    def _update_alien_bullets(self):
        """Update the position of alien bullets and get rid of old bullets"""
        self.alien_bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)

        # Check for bullet-ship collisions
        if pygame.sprite.spritecollideany(
            self.ship, self.alien_bullets, collided=self._hitbox_collision):
            self._ship_hit(bullet)



    
    def _hitbox_collision(self, sprite1, sprite2):
        """Check for collisions between hitboxes"""
        return sprite1.hitbox.rect.colliderect(sprite2.hitbox.rect)


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


    def _ship_hit(self, bullet=None):
        """Respond to the ship being hit by an alien"""

        # Trigger explosion animation
        explosion = DeathEffect(self, self.ship.rect.center, 
                                    'assets/explosion.png', 6, 
                                    self.settings.ship_width, 
                                    self.settings.ship_height)
        self.death_effects.add(explosion)

        self.ship.rect.midbottom = (-100, -100)

        # Remove alien bullet if it hit the ship
        if bullet:
            self.alien_bullets.remove(bullet)

        self._pause_game_for_explosion()

        if self.stats.ships_left > 0:
            # Decrement ships left and update scoreboard
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()
            self.ship.center_ship()
        else:
            self.game_active = False
            self.game_over = True
            pygame.mouse.set_visible(True)

    
    def _reset_level(self):
        """Clear existing bullets/aliens, reset the fleet and center the ship"""
        # Get rid of any remaining bullets and aliens
        self.bullets.empty()
        self.aliens.empty()
        self.alien_bullets.empty()

        # Create a new fleet and center ship
        self._create_fleet()
        self.ship.center_ship()

    
    def _pause_game_for_explosion(self):
        """Pause the game and play the explosion animation"""
        self.player_death_sound.play()
        while any(explosion.alive() for explosion in self.death_effects):
            self.death_effects.update()
            self._update_screen()
            self.clock.tick(100)


    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _create_fleet(self):
        """Create a fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self, 'assets/alan.png', 6)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the fleet of aliens
        for row_number in range(number_rows):
            # Choose a sprite sheet and number of frames for the current row
            if row_number % 3 == 0:
                sprite_sheet_path = 'assets/alan.png'
                num_frames = 6
            elif row_number % 3 == 1:
                sprite_sheet_path = 'assets/bon_bon.png'
                num_frames = 4
            else:
                sprite_sheet_path = 'assets/lips.png'
                num_frames = 5

            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number, sprite_sheet_path, num_frames)
    

    def _create_alien(self, alien_number, row_number, sprite_sheet_path, num_frames):
        """Create an alien and place it in the row"""
        alien = Alien(self, sprite_sheet_path, num_frames)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.5 * alien.rect.height * row_number
        self.aliens.add(alien)
    

    def _prep_difficulty_text(self):
        """Prepare the 'Difficulty' text"""
        self.difficulty_image = self.font.render("Difficulty", 
                                                 True, (255, 255, 255))
        self.difficulty_rect = self.difficulty_image.get_rect()
        self.difficulty_rect.centerx = self.screen.get_rect().centerx
        self.difficulty_rect.top = self.easy_button.rect.top - 80  


    def _prep_game_over_message(self):
        """Prepare the 'Game Over' message"""
        self.game_over_image = self.font.render("Game Over", True, (255, 0, 0))
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.center = self.screen.get_rect().center
        self.game_over_rect.y -= 100

    
    def _draw_difficulty_text(self):
        """Draw the 'Difficulty' text to the screen"""
        self.screen.blit(self.difficulty_image, self.difficulty_rect)


    def _draw_game_over_message(self):
        """Draw the 'Game Over' message to the screen"""
        self.screen.blit(self.game_over_image, self.game_over_rect)


    def _update_screen(self):
        """Update the images on the screen, and flip to the new screen"""
        # Draw background image
        self.screen.blit(self.bg_image, (0,0))

        if self.game_active:
            self.ship.blitme()
            self.aliens.draw(self.screen)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.alien_bullets.sprites():
                bullet.draw_bullet()
            for death_effect in self.death_effects.sprites():
                death_effect.draw()
                    
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

        if not self.game_active and not self.waiting_for_difficulty and not self.game_over and not self.how_to_play_screen:
            self._draw_main_menu()
        elif self.paused:
            self._draw_pause_menu()
            pygame.mouse.set_visible(True)

        if self.how_to_play_screen:
            self._draw_how_to_play()

        pygame.display.flip()

    
    def _draw_main_menu(self):
        """Draw the main menu"""
        self.screen.blit(self.logo_image, self.logo_rect) 
        self.play_button.draw_button()
        self.how_to_play_button.draw_button()
        self.settings_button_main.draw_button()
        self.quit_button_main.draw_button()


    def _draw_how_to_play(self):
        """Draw the 'How to Play' screen"""
        self.screen.blit(self.bg_image, (0, 0))

        # Title
        title_text = self.font.render("How to Play", True, (255, 255, 0))
        title_rect = title_text.get_rect()
        title_rect.centerx = self.screen.get_rect().centerx
        title_rect.top = 100
        self.screen.blit(title_text, title_rect)

        # Objective
        objective_text = self.small_font.render("Destroy the fleet of aliens before they reach the bottom of the screen", True, (255, 255, 255))
        objective_rect = objective_text.get_rect()
        objective_rect.centerx = self.screen.get_rect().centerx
        objective_rect.top = 150
        self.screen.blit(objective_text, objective_rect)

        objective_text = self.small_font.render("Don't let the aliens destroy your spaceship", True, (255, 255, 255))
        objective_rect = objective_text.get_rect()
        objective_rect.centerx = self.screen.get_rect().centerx
        objective_rect.top = 190
        self.screen.blit(objective_text, objective_rect)

        objective_text2 = self.small_font.render("Alien speed and fleet size increases as you progress through the levels", True, (255, 255, 255))
        objective_rect2 = objective_text2.get_rect()
        objective_rect2.centerx = self.screen.get_rect().centerx
        objective_rect2.top = 230
        self.screen.blit(objective_text2, objective_rect2)

        # Controls
        controls_text = self.font.render("Controls", True, (255, 255, 0))
        controls_rect = controls_text.get_rect()
        controls_rect.centerx = self.screen.get_rect().centerx
        controls_rect.top = 300
        self.screen.blit(controls_text, controls_rect)

        move_left_text = self.small_font.render("Move Left - Left Arrow Key", True, (255, 255, 255))
        move_left_rect = move_left_text.get_rect()
        move_left_rect.centerx = self.screen.get_rect().centerx
        move_left_rect.top = 340
        self.screen.blit(move_left_text, move_left_rect)

        move_right_text = self.small_font.render("Move Right - Right Arrow Key", True, (255, 255, 255))
        move_right_rect = move_right_text.get_rect()
        move_right_rect.centerx = self.screen.get_rect().centerx
        move_right_rect.top = 380
        self.screen.blit(move_right_text, move_right_rect)

        shoot_text = self.small_font.render("Shoot - Spacebar", True, (255, 255, 255))
        shoot_rect = shoot_text.get_rect()
        shoot_rect.centerx = self.screen.get_rect().centerx
        shoot_rect.top = 420
        self.screen.blit(shoot_text, shoot_rect)

        pause_text = self.small_font.render("Pause - Escape", True, (255, 255, 255))
        pause_rect = pause_text.get_rect()
        pause_rect.centerx = self.screen.get_rect().centerx
        pause_rect.top = 460
        self.screen.blit(pause_text, pause_rect)

        quit_text = self.small_font.render('Press "q" at any time to close the game', True, (255, 255, 255))
        quit_rect = quit_text.get_rect()
        quit_rect.centerx = self.screen.get_rect().centerx
        quit_rect.top = 500
        self.screen.blit(quit_text, quit_rect)

        self.back_button.draw_button()


    def _draw_pause_menu(self):
        """Draw the pause menu"""
        pause_text = self.font.render("Game Paused", True, (255, 255, 255))
        pause_rect = pause_text.get_rect()
        pause_rect.center = self.screen.get_rect().center
        pause_rect.y -= 200
        self.screen.blit(pause_text, pause_rect)

        self.resume_button.draw_button()
        self.how_to_play_button.draw_button()
        self.settings_button.draw_button()
        self.main_menu_button.draw_button()


if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
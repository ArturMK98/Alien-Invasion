import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.text_colour = (30, 30, 30)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score(initial=True)
        self.prep_level()
        self.prep_ships()

    
    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_colour,
                                            None)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self, initial=False):
        """Turn the high score into a rendered image"""
        if initial:
            high_score = 0
        else:
            difficulty = self.settings.difficulty
            high_score = self.stats.high_scores[difficulty]

        high_score = round(high_score, -1)
        high_score_str = f"High Score: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, 
                                                 self.text_colour, None)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(level_str, True, self.text_colour,
                                           None)

        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def show_game_info(self):
        """Draw score,level and lives to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    
    def check_high_score(self):
        """Check to see if there's a new high score"""
        difficulty = self.settings.difficulty
        if self.stats.score > self.stats.high_scores[difficulty]:
            self.stats.high_scores[difficulty] = self.stats.score
            self.prep_high_score()
            self.stats.save_high_scores()

    
    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            # Scale down the ship image
            ship.image = pygame.transform.scale(
                ship.image, (int(ship.rect.width * 0.5), 
                             int(ship.rect.height * 0.5)))
            ship.rect = ship.image.get_rect()
            ship.rect.x = 10 + ship_number * (ship.rect.width + 10)
            ship.rect.y = 10
            self.ships.add(ship)
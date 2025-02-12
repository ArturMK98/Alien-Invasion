class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800

        # Ship settings
        self.ship_limit = 3
        self.ship_width = 60
        self.ship_height = 60

        # Bullet settings
        self.bullet_width = 20
        self.bullet_height = 60
        self.alien_bullet_width = 50
        self.alien_bullet_height = 50

        # Alien settings
        self.alien_width = 70
        self.alien_height = 70
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the point values increase
        self.score_scale = 1.5

        # Death animation settings
        self.death_effect_width = 70
        self.death_effect_height = 70

        self.initialize_dynamic_settings()

    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 4.5
        self.bullet_speed = 5.5

        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring settings
        self.alien_points = 50
        
    def increase_values(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)


    def set_easy_mode(self):
        """Set settings for easy mode"""
        self.alien_speed = 2.0
        self.difficulty = 'easy'
        self.bullets_allowed = 3
        self.alien_shoot_frequency = 0.01
        

    def set_medium_mode(self):
        """Set settings for medium mode"""
        self.alien_speed = 2.5
        self.difficulty = 'medium'
        self.bullets_allowed = 2
        self.alien_shoot_frequency = 0.03


    def set_hard_mode(self):
        """Set settings for hard mode"""
        self.alien_speed = 3.0
        self.difficulty = 'hard'
        self.bullets_allowed = 1
        self.alien_shoot_frequency = 0.5

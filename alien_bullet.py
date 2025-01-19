from bullet import Bullet

class AlienBullet(Bullet):
    """A class to manage bullets fired by aliens"""

    def __init__(self, ai_game, alien, sprite_sheet_path, num_frames):
        """Create a bullet object at the alien's current position"""
        super().__init__(ai_game, sprite_sheet_path, num_frames)

        # Start the bullet at the alien's current position
        self.rect.midtop = alien.rect.midbottom

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet down the screen and animate"""
        # Update the decimal position of the bullet
        self.y += self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
        # Animate the bullet
        self._animate()
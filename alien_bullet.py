from bullet import Bullet
from hitbox import Hitbox

class AlienBullet(Bullet):
    """A class to manage bullets fired by aliens"""

    def __init__(self, ai_game, alien, sprite_sheet_path, num_frames):
        """Create a bullet object at the alien's current position"""
        super().__init__(ai_game, sprite_sheet_path, num_frames)

         # Scale the frames if needed
        self.frames = self._scale_frames(self.frames, 
                                         self.settings.alien_bullet_width, 
                                         self.settings.alien_bullet_height)
        

        # Set the initial frame
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Start the bullet at the alien's current position
        self.rect.midtop = alien.rect.midbottom

        # Create a separate hitbox with custom size
        self.hitbox = Hitbox(self.settings.alien_bullet_width * 0.4,
                             self.settings.alien_bullet_height * 0.33, 
                             self.rect.center) 

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet down the screen and animate"""
        # Update the decimal position of the bullet
        self.y += self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
        # Animate the bullet
        self.hitbox.update(self.rect.center)

        self._animate()

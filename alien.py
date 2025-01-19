import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('assets/Alan.png')
        self.frames = self._extract_frames(self.sprite_sheet, 4)

        # Set the initial frame
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Start each new alien near the top of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

        # Animation settings
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()


    def _extract_frames(self, sprite_sheet, num_frames):
        """Extract frames from a sprite sheet"""
        frames = []
        sheet_rect = sprite_sheet.get_rect()
        frame_width = sheet_rect.width // num_frames
        frame_height = sheet_rect.height

        for i in range(num_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(
                i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)

        return frames

    
    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)


    def update(self):
        """Move the alien to the right or left"""
        self._animate()
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    
    def _animate(self):  # New method
        """Animate the alien"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    

    

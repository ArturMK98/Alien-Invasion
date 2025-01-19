import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self, ai_game, sprite_sheet_path, num_frames):
        """Initialize the ship and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect
        # Load the sprite sheet and extract frames
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)
        self.frames = self._extract_frames(self.sprite_sheet, num_frames)

        # Scale the frames
        self.frames = [
            pygame.transform.scale(
                frame, (self.settings.ship_width, self.settings.ship_height)
                ) for frame in self.frames]

        # Set the initial frame
        self.current_frame = 1
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position
        self.x = float(self.rect.x)

        # Movement flag; start with a ship that is not moving
        self.moving_right = False
        self.moving_left = False

        # Animation settings
        self.animation_speed = 0.2
        self.last_update = pygame.time.get_ticks()

    def _extract_frames(self, sprite_sheet, num_frames):  # New method to extract frames
        """Extract individual frames from the sprite sheet"""
        frames = []
        sheet_rect = sprite_sheet.get_rect()
        frame_width = sheet_rect.width // num_frames
        frame_height = sheet_rect.height

        for i in range(num_frames):
            frame = sprite_sheet.subsurface(
                pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)

        return frames


    def update(self):
        """Update the ship's position based on the movement flag"""
        # Update the ship's x value, not the rect
        if self.moving_right and not self.moving_left and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
            self.current_frame = 2
        elif self.moving_left and not self.moving_right and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            self.current_frame = 0
        else:
            self.current_frame = 1
            
        # Update rect object from self.x
        self.rect.x = self.x

        # Update image to the current frame
        self.image = self.frames[self.current_frame]


    def _animate(self):
        """Animate the ship"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]


    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    
    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game, sprite_sheet_path, num_frames):
        """Create a bullet object at the ship's current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Load the sprite sheet and extract frames
        self.image = pygame.image.load(sprite_sheet_path)
        self.frames = self._extract_frames(self.image, num_frames)

        # Scale the frames if needed
        self.frames = [
            pygame.transform.scale(
                frame, (self.settings.bullet_width, self.settings.bullet_height)
                ) for frame in self.frames]
        
        # Set the initial frame
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Start the bullet at the ship's current position
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # Store the bullet's position as a float
        self.y = float(self.rect.y)
        print(self.rect)

        # Animation settings
        self.animation_speed = 0.1  # Adjust as needed
        self.last_update = pygame.time.get_ticks()

    
    def _extract_frames(self, image, num_frames):
        """Extract individual frames from the sprite sheet"""
        frames = []
        sheet_rect = image.get_rect()
        frame_width = sheet_rect.width // num_frames
        frame_height = sheet_rect.height

        for i in range(num_frames):
            frame = image.subsurface(
                pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)

        return frames


    def update(self):
        """Move the bullet up the screen"""
        # Update the exact position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

        # Animate the bullet
        self._animate()


    def _animate(self):
        """Animate the bullet"""
        now = pygame.time.get_ticks() 
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
    
    
    def draw_bullet(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.image, self.rect)
        self._draw_hitbox()


    def _draw_hitbox(self):
        """Draw the hitbox for visualization"""
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 1)
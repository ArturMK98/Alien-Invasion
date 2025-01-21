import pygame
from pygame.sprite import Sprite

class DeathEffect(Sprite):
    """A class to death effect animations"""

    def __init__(self, ai_game, center, sprite_sheet_path, num_frames, width, height):
        """Initialize the explosion animation"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the sprite sheet and extract frames
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)
        self.frames = self._extract_frames(self.sprite_sheet, num_frames)

        # Scale the frames if needed
        self.frames = [
            pygame.transform.scale(
                frame, (width, height) ) for frame in self.frames]

        # Set the initial frame
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = center

        # Animation settings
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()


    def _extract_frames(self, sprite_sheet, num_frames):
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
        """Update the death effect animation"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame < len(self.frames):
                self.image = self.frames[self.current_frame]
            else:
                self.kill()


    def draw(self):
        """Draw the death effect to the screen"""
        self.screen.blit(self.image, self.rect)
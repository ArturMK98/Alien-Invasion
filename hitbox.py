import pygame

class Hitbox:
    """A class to manage a hitbox"""

    def __init__(self, width, height, center):
        """Initialize the hitbox with a specific size and center position"""
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center


    def update(self, center):
        """Update the hitbox position"""
        self.rect.center = center


    def draw(self, screen):
        """Draw the hitbox for visualization"""
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
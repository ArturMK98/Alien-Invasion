import pygame

class Slider:
    """A class to create a slider for adjusting settings"""

    def __init__(self, ai_game, label, min_value=0, max_value=100, y_offset=0):
        """Initialize the slider"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.label = label
        self.min_value = min_value
        self.max_value = max_value
        self.value = max_value

        # Slider dimensions
        self.width = 300
        self.height = 20
        self.slider_color = (200, 200, 200)
        self.knob_color = (100, 100, 100)
        self.label_color = (255, 255, 255)
        self.font = pygame.font.Font('assets/ThaleahFat.ttf', 36)

        # Position the slider
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery + y_offset

        # Position the knob
        self.knob_rect = pygame.Rect(0, 0, self.height, self.height)
        self.knob_rect.center = self.rect.center
        self.knob_rect.centerx = self.rect.right

        # Label
        self.label_image = self.font.render(self.label, True, self.label_color)
        self.label_rect = self.label_image.get_rect()
        self.label_rect.centerx = self.rect.centerx
        self.label_rect.bottom = self.rect.top - 10

        self.dragging = False

    def draw_slider(self):
        """Draw the slider and knob"""
        pygame.draw.rect(self.screen, self.slider_color, self.rect)
        pygame.draw.rect(self.screen, self.knob_color, self.knob_rect)
        self.screen.blit(self.label_image, self.label_rect)

        # Draw the volume percentage above the slider
        volume_percentage = f"{int(self.get_value())}%"
        volume_text = self.font.render(volume_percentage, True, self.label_color)
        volume_rect = volume_text.get_rect()
        volume_rect.centerx = self.rect.centerx
        volume_rect.bottom = self.label_rect.top + 100
        self.screen.blit(volume_text, volume_rect)

    def handle_event(self, event):
        """Handle mouse events for the slider"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.knob_rect.centerx = max(self.rect.left, 
                                             min(event.pos[0], self.rect.right))
                self.value = self.min_value + (
                    self.max_value - self.min_value) * (
                        self.knob_rect.centerx - self.rect.left) / self.width

    def get_value(self):
        """Return the current value of the slider"""
        return self.value
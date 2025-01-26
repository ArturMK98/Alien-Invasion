import pygame.font

def draw_rounded_rect(surface, rect, color, radius=10):
    """Draw a rounded rectangle"""
    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0

    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size)*3]*2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(circle, [int(min(rect.size)*0.5)]*2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

    rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)


class Button:
    """A class to build buttons for the game"""

    def __init__(self, ai_game, msg, y_offset=0):
        """Initialize button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_colour = (87, 188, 43)
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.Font('assets/ThaleahFat.ttf', 30)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y += y_offset

        # The button message needs to be prepped only once
        self._prep_msg(msg)


    def _prep_msg(self, msg):
        """Turn msg into a rendered image & center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_colour, 
                                          None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        

    def draw_button(self):
        """Draw button and message"""
        # Draw the outline
        outline_rect = self.rect.inflate(5, 5)
        draw_rounded_rect(self.screen, outline_rect, (0, 0, 0), radius=10)
        # outline_rect = self.rect.inflate(4, 4)
        # pygame.draw.rect(self.screen, (0, 0, 0), outline_rect, 2)

        # Draw the button
        draw_rounded_rect(self.screen, self.rect, self.button_colour, radius=10)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        # self.screen.fill(self.button_colour, self.rect)
        # self.screen.blit(self.msg_image, self.msg_image_rect)
                




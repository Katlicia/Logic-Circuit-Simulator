import pygame

class Button:
    def __init__(self, x, y, width, height, text = None, font_size = 30, color = "black", text_color = "white"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.text_color = text_color
        self.active = False

    def draw(self, surface):
        if self.text != None:
            pygame.draw.rect(surface, self.color, self.rect)
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center = self.rect.center)
            surface.blit(text_surface, text_rect)

    def isClicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def setColor(self, color):
        self.color = color

    def setActive(self, active):
        self.active = active
        self.color = "grey" if active else "black"
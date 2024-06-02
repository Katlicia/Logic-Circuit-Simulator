import pygame

class Fastener:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.output_count = 0
        self.value = 0

    def draw(self, surface):
        raise NotImplementedError("This method should be implemented by subclasses")

    def rect(self):
        raise NotImplementedError("This method should be implemented by subclasses")

class Line(Fastener):
    icon = pygame.image.load("tools/fasteners/line.png")
    icon = pygame.transform.scale(icon, (50, 50))

    def draw(self, surface):
        surface.blit(Line.icon, (self.x, self.y))
    
    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

class Node(Fastener):
    icon = pygame.image.load("tools/fasteners/node.png")
    icon = pygame.transform.scale(icon, (50, 50))



    def draw(self, surface):
        surface.blit(Node.icon, (self.x, self.y))
    
    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)
    
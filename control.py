import pygame

class Control:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, surface):
        raise NotImplementedError("This method should be implemented by subclasses")

    def rect(self):
        raise NotImplementedError("This method should be implemented by subclasses")

class Reset(Control):
    icon = pygame.image.load("tools/controls/reset.png")
    icon = pygame.transform.scale(icon, (50, 50))

    def draw(self, surface):
        surface.blit(Reset.icon, (self.x, self.y))
    
    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

class Run(Control):
    icon = pygame.image.load("tools/controls/run.png")
    icon = pygame.transform.scale(icon, (50, 50))

    def draw(self, surface):
        surface.blit(Run.icon, (self.x, self.y))
    
    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

class Stop(Control):
    icon = pygame.image.load("tools/controls/stop.png")
    icon = pygame.transform.scale(icon, (50, 50))

    def draw(self, surface):
        surface.blit(Stop.icon, (self.x, self.y))
    
    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)
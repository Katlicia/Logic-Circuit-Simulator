import pygame

class Gate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inputs = []
        self.output = None
        self.input_count = 0

    def draw(self, surface):
        raise NotImplementedError("This method should be implemented by subclasses")

    def add_input(self, value):
        self.inputs.append(value)

    def compute_output(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    def rect(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    def get_port_position(self, port_index):
        if port_index == 0:
            return (self.x, self.y + 15)
        elif port_index == 1:
            return (self.x, self.y + 35)
        elif port_index == 2:
            return (self.x + 50, self.y + 25)
        
# Alt sınıflar
class NotGate(Gate):
    icon = pygame.image.load("tools/gates/brownnot.png")
    icon = pygame.transform.scale(icon, (50, 50))
    max_input = 1

    def draw(self, surface):
        surface.blit(NotGate.icon, (self.x, self.y))

    def compute_output(self):
        self.output = not self.inputs[0]
    
    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)


class BufferGate(Gate):
    icon = pygame.image.load("tools/gates/purplebuffer.png")
    icon = pygame.transform.scale(icon, (50, 50))
    max_input = 1

    def draw(self, surface):
        surface.blit(BufferGate.icon, (self.x, self.y))

    def compute_output(self):
        self.output = self.inputs[0]

    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)


class AndGate(Gate):
    icon = pygame.image.load("tools/gates/redand.png")
    icon = pygame.transform.scale(icon, (50, 50))
    max_input = 2

    def draw(self, surface):
        surface.blit(AndGate.icon, (self.x, self.y))

    def compute_output(self):
        if self.inputs[0] + self.inputs[1] == 2:
            self.output = 1
        else:
            self.output = 0

    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

class OrGate(Gate):
    icon = pygame.image.load("tools/gates/cyanor.png")
    icon = pygame.transform.scale(icon, (50, 50))
    max_input = 2

    def draw(self, surface):
        surface.blit(OrGate.icon, (self.x, self.y))

    def compute_output(self):
        if self.inputs[0] + self.inputs[1] == 0:
            self.output = 0
        else:
            self.output = 1

    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

class NandGate(Gate):
    icon = pygame.image.load("tools/gates/bluenand.png")
    icon = pygame.transform.scale(icon, (50, 50))
    max_input = 2

    def draw(self, surface):
        surface.blit(NandGate.icon, (self.x, self.y))

    def compute_output(self):
        if self.inputs[0] + self.inputs[1] == 2:
            self.output = 0
        else:
            self.output = 1

    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

class NorGate(Gate):
    icon = pygame.image.load("tools/gates/greennor.png")
    icon = pygame.transform.scale(icon, (50, 50))
    max_input = 2

    def draw(self, surface):
        surface.blit(NorGate.icon, (self.x, self.y))

    def compute_output(self):
        if self.inputs[0] + self.inputs[1] == 0:
            self.output = 1
        else:
            self.output = 0

    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

class XorGate(Gate):
    icon = pygame.image.load("tools/gates/lightxor.png")
    icon = pygame.transform.scale(icon, (50, 50))
    max_input = 2

    def draw(self, surface):
        surface.blit(XorGate.icon, (self.x, self.y))

    def compute_output(self):
        if self.inputs[0] + self.inputs[1] == 1:
            self.output = 1
        else:
            self.output = 0

    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

class XnorGate(Gate):
    icon = pygame.image.load("tools/gates/darkxnor.png")
    icon = pygame.transform.scale(icon, (50, 50))
    max_input = 2

    def draw(self, surface):
        surface.blit(XnorGate.icon, (self.x, self.y))

    def compute_output(self):
        if self.inputs[0] + self.inputs[1] == 1:
            self.output = 0
        else:
            self.output = 1

    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)
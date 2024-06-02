import pygame

class IOElements:
    def __init__(self, x, y, value = 0):
        self.x = x
        self.y = y
        self.value = value
        self.input_count = None
        self.output_count = None

    def draw(self, surface):
        raise NotImplementedError("This method should be implemented by subclasses")

    def rect(self):
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def connection(self):
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def get_port_position(self, port_index):
        if port_index == 0:  
            return (self.x, self.y + 15)
        elif port_index == 1:
            return (self.x, self.y + 35)
        elif port_index == 2:
            return (self.x + 50, self.y + 25)

class InputBox(IOElements):
    icon = pygame.image.load("tools/io/input.png")
    icon = pygame.transform.scale(icon, (50, 50))

    def __init__(self, x, y, value = 0):
        super().__init__(x, y, value)
        self.input_count = 0
        self.output_count = 0

    def draw(self, surface):
        surface.blit(InputBox.icon, (self.x, self.y))
    
    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

    def connection(self):
        if self.input_count != 0:
            raise ValueError("Input Box can't have input.")
        elif self.output_count != 1:
            raise ValueError("Input Box must have exactly one output.")

class OutputBox(IOElements):
    icon = pygame.image.load("tools/io/output.png")
    icon = pygame.transform.scale(icon, (50, 50))

    def __init__(self, x, y, value = 0):
        super().__init__(x, y, value)
        self.input_count = 0
        self.output_count = 0

    def draw(self, surface):
        surface.blit(OutputBox.icon, (self.x, self.y))

    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

    def connection(self):
        if self.input_count < 1:
            raise ValueError("Output Box must have at least one input.")
        elif self.output_count != 1:
            raise ValueError("Output Box can't have input.")

class Led(IOElements):
    icon_on = pygame.image.load("tools/io/ledon.png")
    icon_on = pygame.transform.scale(icon_on, (50, 50))
    icon_off = pygame.image.load("tools/io/ledoff.png")
    icon_off = pygame.transform.scale(icon_off, (50, 50))


    def __init__(self, x, y, value = 0):
        super().__init__(x, y, value)
        self.input_count = 0
        self.output_count = 0

    def draw(self, surface):
        if self.value == 0:
            surface.blit(Led.icon_off, (self.x, self.y))
        else:
            surface.blit(Led.icon_on, (self.x, self.y))

    def rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)
     
    def connection(self):
        if self.input_count != 1:
            raise ValueError("Led must have exactly one input.")
        elif self.output_count != 1:
            raise ValueError("Led can't have input.")
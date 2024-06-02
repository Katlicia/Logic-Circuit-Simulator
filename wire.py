import pygame

class Wire:
    def __init__(self, start_gate, start_port, end_gate, end_port):
        self.start_gate = start_gate
        self.start_port = start_port
        self.end_gate = end_gate
        self.end_port = end_port

    def draw(self, surface):
        start_pos = self.start_gate.get_port_position(self.start_port)
        end_pos = self.end_gate.get_port_position(self.end_port)
        pygame.draw.line(surface, "black", start_pos, end_pos, 3)

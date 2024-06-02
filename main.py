import pygame
from button import *
from gate import *
from ioput import *
from fastener import *
from control import *
from wire import *

pygame.init()

# UI Width Height Variables
WIDTH, HEIGHT = 1920, 1080
MENU_HEIGHT = 30
BUTTON_WIDTH = 110
BUTTON_HEIGHT = MENU_HEIGHT
GATE_GAP = 55
GRID_SIZE = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

# Control Variables
active_button = None
dragging_gate = None
dragging_button = None
dragging_element = None
dragging_fastener = None
dragging_control = None
offset_x, offset_y = 0, 0
line_mode = False
mouse_icon = pygame.image.load("tools/fasteners/line.png")
mouse_icon = pygame.transform.scale(mouse_icon, (30, 30))
is_drawing_line = False
on_or_off = 0

# Fonts
font = pygame.font.Font(None, 30)

# Functions
def drawInputBox(surface, value, x, y):
    rect = pygame.Rect(x, y, 50 + GATE_GAP, 25)
    pygame.draw.rect(surface, "black", rect)
    text = font.render(f"{value}", True, "white")
    screen.blit(text, (x + 3, y + 3))

def drawError(surface):
        rect = pygame.Rect(WIDTH // 2 - 150, 100, 300, 50)
        pygame.draw.rect(surface, "black", rect)
        font = pygame.font.Font(None, 40)
        text_surface = font.render("Value must be 0 or 1", True, "white")
        text_rect = text_surface.get_rect(center = rect.center)
        surface.blit(text_surface, text_rect)

def drawGrid(surface):
    if GRID_SIZE != 0:
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(surface, "grey", (x, MENU_HEIGHT), (x, HEIGHT))
        for y in range(MENU_HEIGHT, HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, "grey", (0, y), (WIDTH, y))

def changeGridSize(delta):
    global GRID_SIZE
    if delta > 0 and GRID_SIZE < 100:
        GRID_SIZE += 25
    elif delta < 0 and GRID_SIZE > 0:
        GRID_SIZE -= 25

def snapToGrid(pos):
    if GRID_SIZE != 0:
        x, y = pos
        snapped_x = x // GRID_SIZE * GRID_SIZE
        snapped_y = ((y - MENU_HEIGHT) // GRID_SIZE) * GRID_SIZE + MENU_HEIGHT
        return snapped_x, snapped_y
    else:
        return pos

def snapGateToGrid(gate):
    if GRID_SIZE != 0:
        gate.x = ((gate.x + GRID_SIZE // 2) // GRID_SIZE) * GRID_SIZE
        gate.y = (((gate.y - MENU_HEIGHT) + GRID_SIZE // 2) // GRID_SIZE) * GRID_SIZE + MENU_HEIGHT

# Clean Button
clean_button = Button(WIDTH - 100, HEIGHT - 50, 75, BUTTON_HEIGHT, "Clean")

# Menu Button List
buttons = [
    Button(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT, "Gates"),
    Button(0 + BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT, "I/O"),
    Button(0 + 2 * BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT, "Fasteners"),
    Button(0 + 3 * BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT, "Control"),
    Button(0 + 4 * BUTTON_WIDTH, 0, BUTTON_WIDTH, BUTTON_HEIGHT, "Grid"),
]

# Grid Button List
grid_buttons = [
    Button(0, MENU_HEIGHT, 50, 50, "100", color = "white", text_color = "black"),
    Button(50, MENU_HEIGHT, 50, 50, "75", color = "white", text_color = "black"), 
    Button(100, MENU_HEIGHT, 50, 50, "50", color = "white", text_color = "black"),
    Button(150, MENU_HEIGHT, 50, 50, "25", color = "white", text_color = "black"),
    Button(200, MENU_HEIGHT, 50, 50, "Off", color = "white", text_color = "black")
]

# Gate Icon List
gate_icons = [
    NotGate(10, MENU_HEIGHT + 5),
    BufferGate(10 + GATE_GAP, MENU_HEIGHT + 5),
    AndGate(10 + GATE_GAP * 2, MENU_HEIGHT + 5),
    OrGate(10 + GATE_GAP * 3, MENU_HEIGHT + 5),
    NandGate(10 + GATE_GAP * 4, MENU_HEIGHT + 5),
    NorGate(10 + GATE_GAP * 5, MENU_HEIGHT + 5),
    XorGate(10 + GATE_GAP * 6, MENU_HEIGHT + 5),
    XnorGate(10 + GATE_GAP * 7, MENU_HEIGHT + 5)
]

gate_buttons = [
    Button(10, MENU_HEIGHT + 60, 50, 25, "NOT", 25),
    Button(10 + GATE_GAP, MENU_HEIGHT + 60, 50, 25, "BFR", 25),
    Button(10 + GATE_GAP * 2, MENU_HEIGHT + 60, 50, 25, "AND", 25),
    Button(10 + GATE_GAP * 3, MENU_HEIGHT + 60, 50, 25, "OR", 25),
    Button(10 + GATE_GAP * 4, MENU_HEIGHT + 60, 50, 25, "NAND", 25),
    Button(10 + GATE_GAP * 5, MENU_HEIGHT + 60, 50, 25, "NOR", 25),
    Button(10 + GATE_GAP * 6, MENU_HEIGHT + 60, 50, 25, "XOR", 25),
    Button(10 + GATE_GAP * 7, MENU_HEIGHT + 60, 50, 25, "XNOR", 25)
]

io_icons = [
    OutputBox(10, MENU_HEIGHT + 5),
    InputBox(10 + GATE_GAP, MENU_HEIGHT + 5), 
    Led(10 + GATE_GAP * 2, MENU_HEIGHT + 5)   
]

io_buttons = [
    Button(10, MENU_HEIGHT + 60, 50, 25, "Out", 25),
    Button(10 + GATE_GAP, MENU_HEIGHT + 60, 50, 25, "In", 25),
    Button(10 + GATE_GAP * 2, MENU_HEIGHT + 60, 50, 25, "Led", 25)
]

fastener_icons = [
    Line(10, MENU_HEIGHT + 5),
    Node(10 + GATE_GAP, MENU_HEIGHT + 5)
]

fastener_buttons = [
    Button(10, MENU_HEIGHT + 60, 50, 25, "Line", 25),
    Button(10 + GATE_GAP, MENU_HEIGHT + 60, 50, 25, "Node", 25)
]

control_icons = [
    Reset(10, MENU_HEIGHT + 5),
    Run(10 + GATE_GAP, MENU_HEIGHT + 5),
    Stop(10 + GATE_GAP * 2, MENU_HEIGHT + 5),
]

control_buttons = [
    Button(10, MENU_HEIGHT + 60, 50, 25, "Reset", 25),
    Button(10 + GATE_GAP, MENU_HEIGHT + 60, 50, 25, "Run", 25),
    Button(10 + GATE_GAP * 2, MENU_HEIGHT + 60, 50, 25, "Stop", 25)
]

# Created Items (By User)
created_gates = []
created_elements = []
created_fasteners = []
created_buttons = []
created_output_button = []
created_output = []
created_logic = []
wire_list = []

# Value and Error Text
value = ""
error = False
error2 = False
drawing_input = False


while running:
    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mousewheel Event for Dynamic Grid Size
        elif event.type == pygame.MOUSEWHEEL: 
            changeGridSize(event.y)
            for gate in created_gates:
                snapGateToGrid(gate)
            for element in created_elements:
                snapGateToGrid(element)
            for fastener in created_fasteners:
                snapGateToGrid(fastener)

        # Menu Click Events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            pos = pygame.mouse.get_pos()
            clicked_button = None

            for button in buttons:
                if button.isClicked(pos):
                    clicked_button = button
                    break
            
            if clicked_button:
                if active_button:
                    active_button.setActive(False)
                clicked_button.setActive(True)
                active_button = clicked_button

            if clean_button.isClicked(pos):
                created_gates.clear()
                created_elements.clear()
                created_fasteners.clear()
                created_buttons.clear()
                created_output_button.clear()
                created_output.clear()
                drawing_input = False
                is_drawing_line = False
                wire_list.clear()

            # Changes Grid Size With Buttons
            if active_button == buttons[4]:
                for button in grid_buttons:
                    if button.isClicked(pos):
                        try:
                            GRID_SIZE = int(button.text)
                        except ValueError:
                            GRID_SIZE = 0
                        for gate in created_gates:
                            snapGateToGrid(gate)
                        for element in created_elements:
                            snapGateToGrid(element)

            # Control Events
            elif active_button == buttons[3]:
                for button in control_buttons:
                    if button.isClicked(pos):
                        if button.text == "Reset":
                            pass
                        elif button.text == "Run":
                            pass
                        elif button.text == "Stop":
                            pass

            # Fastener Events
            elif active_button == buttons[2]:
                for button in fastener_buttons:
                    if button.isClicked(pos):
                        if button.text == "Line":
                            line_mode = True
                        if button.text == "Node":
                            new_fastener = Node(*snapToGrid((WIDTH // 2, HEIGHT // 2)))
                            fastener_button = Button(new_fastener.x, new_fastener.y, 50, 50, text = "fastener")
                            created_fasteners.append(new_fastener)
                            created_buttons.append(fastener_button)
                            created_logic.append(new_fastener)

            # I/O Element Event
            elif active_button == buttons[1]:
                for button in io_buttons:
                    if button.isClicked(pos):
                        if button.text == "Out":
                            new_element = OutputBox(*snapToGrid((WIDTH // 2, HEIGHT // 2)))
                            element_button = Button(new_element.x, new_element.y, 50, 50, text = "io")
                            created_output_button.append(element_button)
                            created_output.append(new_element)
                        elif button.text == "In":
                            new_element = InputBox(*snapToGrid((WIDTH // 2, HEIGHT // 2)))
                            element_button = Button(new_element.x, new_element.y, 50, 50, text = "io")
                        elif button.text == "Led":
                            new_element = Led(*snapToGrid((WIDTH // 2, HEIGHT // 2)))
                            element_button = Button(new_element.x, new_element.y, 50, 50, text = "io")
                        created_elements.append(new_element)
                        created_buttons.append(element_button)
                        created_logic.append(new_element)

            # Gate Menu Events
            elif active_button == buttons[0]:
                for button in gate_buttons:
                    if button.isClicked(pos):
                        if button.text == "NOT":
                            new_gate = NotGate(*snapToGrid((WIDTH // 2, HEIGHT // 2)))
                            gate_button = Button(new_gate.x, new_gate.y, 50, 50, text = "gate")
                        elif button.text == "BFR":
                            new_gate = BufferGate(*snapToGrid((WIDTH // 2, HEIGHT // 2)))
                            gate_button = Button(new_gate.x, new_gate.y, 50, 50, text = "gate")
                        elif button.text == "AND":
                            new_gate = AndGate(*snapToGrid((WIDTH // 2, HEIGHT // 2)))
                            gate_button = Button(new_gate.x, new_gate.y, 50, 50, text = "gate")
                        elif button.text == "OR":
                            new_gate = OrGate(*snapToGrid((WIDTH // 2, HEIGHT // 2)))
                            gate_button = Button(new_gate.x, new_gate.y, 50, 50, text = "gate")
                        elif button.text == "NAND":
                            new_gate = NandGate(*snapToGrid((WIDTH // 2, HEIGHT // 2)))
                            gate_button = Button(new_gate.x, new_gate.y, 50, 50, text = "gate")
                        elif button.text == "NOR":
                            new_gate = NorGate(*snapToGrid((WIDTH // 2, HEIGHT // 2)))
                            gate_button = Button(new_gate.x, new_gate.y, 50, 50, text = "gate")
                        elif button.text == "XOR":
                            new_gate = XorGate(*snapToGrid((WIDTH // 2, HEIGHT // 2)))
                            gate_button = Button(new_gate.x, new_gate.y, 50, 50, text = "gate")
                        elif button.text == "XNOR":
                            new_gate = XnorGate(*snapToGrid((WIDTH // 2, HEIGHT // 2)))
                            gate_button = Button(new_gate.x, new_gate.y, 50, 50, text = "gate")
                        created_gates.append(new_gate)
                        created_buttons.append(gate_button)
                        created_logic.append(new_gate)

            if not line_mode:
                # Gate Position Events
                if len(created_gates) > 0:
                    for gate in created_gates:
                        gate_rect = gate.rect()
                        if gate_rect.collidepoint(pos):
                            dragging_gate = gate
                            offset_x = gate.x - pos[0]
                            offset_y = gate.y - pos[1]
                            break
                # Button Position Events
                if len(created_buttons) > 0:
                    for button in created_buttons:
                        if button.rect.collidepoint(pos):
                            dragging_button = button.rect
                            offset_x = dragging_button.x - pos[0]
                            offset_y = dragging_button.y - pos[1]
                            break

                # Element Position Events
                if len(created_elements) > 0:
                    for element in created_elements:
                        element_rect = element.rect()
                        if element_rect.collidepoint(pos):
                            dragging_element = element
                            offset_x = element.x - pos[0]
                            offset_y = element.y - pos[1]
                            break

                # Fastener Position Events
                if len(created_fasteners) > 0:
                    for fastener in created_fasteners:
                        fastener_rect = fastener.rect()
                        if fastener_rect.collidepoint(pos):
                            dragging_fastener = fastener
                            offset_x = fastener.x - pos[0]
                            offset_y = fastener.y - pos[1]
                            break

        # Sticks the item to grid when mouse button is not clicked anymore.
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_gate:
                dragging_gate.x, dragging_gate.y = snapToGrid((dragging_gate.x, dragging_gate.y))
            dragging_gate = None

            if dragging_button:
                dragging_button.x, dragging_button.y = snapToGrid((dragging_button.x, dragging_button.y))
            dragging_button = None

            if dragging_element:
                dragging_element.x, dragging_element.y = snapToGrid((dragging_element.x, dragging_element.y))
            dragging_element = None

            if dragging_fastener:
                dragging_fastener.x, dragging_fastener.y = snapToGrid((dragging_fastener.x, dragging_fastener.y))
            dragging_fastener = None

        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if dragging_gate:
                dragging_gate.x = pos[0] + offset_x
                dragging_gate.y = pos[1] + offset_y
            if dragging_button:
                dragging_button.x = pos[0] + offset_x
                dragging_button.y = pos[1] + offset_y
            if dragging_element:
                dragging_element.x = pos[0] + offset_x
                dragging_element.y = pos[1] + offset_y

            if dragging_fastener:
                dragging_fastener.x = pos[0] + offset_x
                dragging_fastener.y = pos[1] + offset_y

                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(created_buttons) >= 1:
                for number, i in enumerate(created_buttons):
                    if i.isClicked(pos):
                        button_number = number
                        if line_mode == True:
                            is_drawing_line = True
        # if is_drawing_line:
        #     for number, i in enumerate(created_buttons):
        #         if i.isClicked(pos):
        #             wire = Wire(created_logic[button_number], 1, created_logic[1], 0)
        #             wire_list.append(wire)
        #             is_drawing_line = False

            if len(created_output_button) > 0:
                for number, i in enumerate(created_output_button):
                    if i.isClicked(pos) and created_output[number].output_count < 1:
                        drawing_input = True

        if drawing_input == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(created_output) >= 1:
                        if created_logic[button_number].output_count != 1:
                            if value not in ["0", "1"]:
                                error = True
                            else:
                                element = created_logic[button_number]
                                element.value = int(value)
                                element.output_count += 1
                                error = False
                                drawing_input = False
                elif event.key == pygame.K_BACKSPACE:
                    value = value[:-1]
                else:
                    value += event.unicode
        

    # Simulation Interface

    screen.fill("white")
    menuRect = pygame.Rect(0, 0, WIDTH, MENU_HEIGHT)
    pygame.draw.rect(screen, "black", menuRect, 0)
    drawGrid(screen)

    # Draws Menu Buttons
    for button in buttons:
        button.draw(screen)

    # Draws Clean Button
    clean_button.draw(screen)

    # Draws Logic Gate Buttons
    if active_button == buttons[0]:
        for gate in gate_icons:
            pygame.draw.rect(screen, "white", gate.rect(), 50)
            pygame.draw.rect(screen, "black", gate.rect(), 2)
            gate.draw(screen)
        for b in gate_buttons:
            b.draw(screen)

    # Draws I/O Element Buttons
    elif active_button == buttons[1]:
        for element in io_icons:
            pygame.draw.rect(screen, "white", element.rect(), 50)
            pygame.draw.rect(screen, "black", element.rect(), 2)
            element.draw(screen)
        for b in io_buttons:
            b.draw(screen)

    # Draws Fastener Buttons
    elif active_button == buttons[2]:
        for fastener in fastener_icons:
            pygame.draw.rect(screen, "white", fastener.rect(), 50)
            pygame.draw.rect(screen, "black", fastener.rect(), 2)
            fastener.draw(screen)
        for b in fastener_buttons:
            b.draw(screen)

    # Draws Control Buttons
    elif active_button == buttons[3]:
        for control in control_icons:
            pygame.draw.rect(screen, "white", control.rect(), 50)
            pygame.draw.rect(screen, "black", control.rect(), 2)
            control.draw(screen)
        for b in control_buttons:
            b.draw(screen)

    # Draws Grid Settings
    elif active_button == buttons[4]:
        for grid in grid_buttons:
            grid.draw(screen)
            pygame.draw.rect(screen, "black", grid.rect, 2)

    # Draws Created Gates
    if len(created_gates) > 0:
        for gate in created_gates:
            gate.draw(screen)

    # Draw Created Elements
    if len(created_elements) > 0:
        for element in created_elements:
            element.draw(screen)

    if len(created_fasteners) > 0:
        for fastener in created_fasteners:
            fastener.draw(screen)

    if line_mode and active_button == buttons[2]:
        x, y = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)
        screen.blit(mouse_icon, (x, y))
    else:
        line_mode = False
        pygame.mouse.set_visible(True)

    if drawing_input:
        drawInputBox(screen, value, fastener_buttons[0].rect.x, fastener_buttons[0].rect.y + 50)
        if error:
            drawError(screen)
    

    # Connects Wires and Computes Gate Values
    if is_drawing_line:
        pygame.draw.line(screen, "black", (created_logic[button_number].x, created_logic[button_number].y), (pos[0], pos[1]), 3)
        for number, i in enumerate(created_buttons):
            if i.isClicked(pos) and i != created_buttons[button_number]:
                wire = Wire(created_logic[button_number], 1, created_logic[number], 0)
                if type(created_logic[button_number]) == Gate and type(created_logic[number]) == OutputBox:
                    created_logic[button_number].inputs.append(created_logic[number].value)
                    created_logic[button_number].input_count += 1
                    if created_logic[button_number].input_count > created_logic[button_number].max_input:
                        created_logic[button_number].output = 0
                    elif created_logic[button_number].input_count == created_logic[button_number].max_input:
                        created_logic[button_number].compute_output() 
                        on_or_off = created_logic[button_number].output
                elif type(created_logic[number] == Gate) and type(created_logic[button_number]) == OutputBox:
                    created_logic[number].inputs.append(created_logic[button_number].value)
                    created_logic[number].input_count += 1
                    if created_logic[number].input_count > created_logic[number].max_input:
                        created_logic[number].output = 0
                    elif created_logic[number].input_count == created_logic[number].max_input:
                        created_logic[number].compute_output()                     
                        on_or_off = created_logic[number].output
                wire_list.append(wire)
                is_drawing_line = False
                if type(created_logic[button_number]) == Gate and type(created_logic[number]) == Led:
                    if on_or_off == 1:
                        created_logic[number].value = 1
                        created_logic[number].draw(screen)
                    else:
                        created_logic[number].value = 0
                        created_logic[number].draw(screen)
                elif type(created_logic[number]) == Gate and type (created_logic[button_number]) == Led:
                    if on_or_off == 1:
                        created_logic[button_number].value = 1,
                        created_logic[button_number].draw(screen)
                    else:
                        created_logic[button_number].value = 0
                        created_logic[button_number].draw(screen)

    for wire in wire_list:
        wire.draw(screen)

    pygame.display.flip()
    clock.tick(144)

pygame.quit()


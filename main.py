import pygame   #main graphics library
import sys  #default python system library

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

pygame.display.set_caption("Digital Logic Sim")

def load_and_make_transparent(filename):
    # Load your JPEG image
    image = pygame.image.load(filename).convert_alpha()
    
    # Create a new surface with the same size and alpha channel
    new_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    
    # Loop through each pixel in the image
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            # Get the color of the pixel
            color = image.get_at((x, y))
            # If the pixel's RGB values are above the threshold, make it transparent
            if color.r > 240 and color.g > 240 and color.b > 240:
                new_surface.set_at((x, y), (0, 0, 0, 0))  # Set transparent
            else:
                new_surface.set_at((x, y), color)  # Keep original color

    # Convert the surface back to an image
    return pygame.image.fromstring(pygame.image.tostring(new_surface, "RGBA"), new_surface.get_size(), "RGBA")


images = []

images.append(load_and_make_transparent("andgate.jpeg"))
images.append(load_and_make_transparent("orgate.jpeg"))
images.append(load_and_make_transparent("notgate.jpeg"))
images.append(load_and_make_transparent("norgate.jpeg"))
images.append(load_and_make_transparent("xorgate.jpeg"))
images.append(load_and_make_transparent("nandgate.jpeg"))


# Component class
class Component:
    def __init__(self, x, y, width, height, singleInput = False):
        self.x = x  # Center x
        self.y = y  # Center y
        self.width = width
        self.height = height
        self.colour = (255,0,220)

        self.singleInput = singleInput

        if self.singleInput:
            self.input1xy = [self.x - self.width//2 - 3, self.y]
        else:
            self.input1xy = [self.x - self.width//2 - 3, self.y - self.height//2 + 13]

        self.input1colour = (105, 105, 100)
        self.input1Val = False

        self.input2xy = [self.x - self.width//2 - 3, self.y - self.height//2 + 43]
        self.input2colour = (105, 105, 100)
        self.input2Val = False

        self.outputxy = [self.x + self.width//2 + 7, self.y]
        self.outputcolour = (105, 105, 100)

        self.outputs = []
        self.outputVal = False

    def draw(self, screen):
        # Calculate the top-left corner based on the center position
        top_left_x = self.x - self.width // 2
        top_left_y = self.y - self.height // 2
        
        # Draw the rectangle
        pygame.draw.rect(screen, self.colour, (top_left_x, top_left_y, self.width, self.height))

    def is_hovered(self, mouse_pos):
        #Check if the mouse is hovering over the rectangle.
        mouse_x, mouse_y = mouse_pos
        
        # Check if the mouse is within the bounds of the rectangle
        if (self.x - self.width // 2 <= mouse_x <= self.x + self.width // 2 and
            self.y - self.height // 2 <= mouse_y <= self.y + self.height // 2):
            return True
        return False
    
    def is_input1_hovered(self, mouse_pos):
        deltax = mouse_pos[0] - self.input1xy[0]
        deltay = mouse_pos[1] - self.input1xy[1]

        #check if the mouse hovering over the input circle
        return (deltax**2 + deltay**2)**0.5 <= 10
    
    def is_input2_hovered(self, mouse_pos):
        if self.singleInput:
            return False
        
        deltax = mouse_pos[0] - self.input2xy[0]
        deltay = mouse_pos[1] - self.input2xy[1]

        #check if the mouse hovering over the input circle
        return (deltax**2 + deltay**2)**0.5 <= 10
    
    def is_output_hovered(self, mouse_pos):
        deltax = mouse_pos[0] - self.outputxy[0]
        deltay = mouse_pos[1] - self.outputxy[1]

        #check if the mouse hovering over the input circle
        return (deltax**2 + deltay**2)**0.5 <= 10
    
    def drawInputs(self, screen):
        pygame.draw.circle(screen, self.input1colour, tuple(self.input1xy), 10, 3)
        if not self.singleInput:
            pygame.draw.circle(screen, self.input2colour, tuple(self.input2xy), 10, 3)
    
    def drawOutputs(self, screen):
        pygame.draw.circle(screen, self.outputcolour, tuple(self.outputxy), 10, 3)
        for compsAndinputs in self.outputs:
            if compsAndinputs[1] == 1:
                pygame.draw.line(screen, self.outputcolour, tuple(self.outputxy), tuple(compsAndinputs[0].input1xy), 2)
            elif compsAndinputs[1] == 2:
                pygame.draw.line(screen, self.outputcolour, tuple(self.outputxy), tuple(compsAndinputs[0].input2xy), 2)


    def UpdatePos(self, mouse_pos):
        self.x = mouse_pos[0]
        self.y = mouse_pos[1]

        if not self.singleInput:
            self.input1xy = [self.x - self.width//2 - 3, self.y - self.height//2 + 13]
            self.input2xy = [self.x - self.width//2 - 3, self.y - self.height//2 + 43]
        else:
            self.input1xy = [self.x - self.width//2 - 3, self.y]
        self.outputxy = [self.x + self.width//2 + 7, self.y]

    #reset the component when the simulation is over
    def reset(self):
        self.input1Val = False
        self.input2Val = False
        self.outputVal = False

    def Simulate(self):
        for compsAndinputs in self.outputs:
            if compsAndinputs[1] == 1:
                compsAndinputs[0].input1Val = self.outputVal
            elif compsAndinputs[1] == 2:
                compsAndinputs[0].input2Val = self.outputVal



class AndGate(Component):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, screen):
        # Scale the sprite to the width and height of the component, then draw
        scaled_sprite = pygame.transform.scale(images[0], (self.width, self.height))
        rect = scaled_sprite.get_rect(center=(self.x, self.y))
        screen.blit(scaled_sprite, rect)
    
    def Simulate(self):
        self.outputVal = self.input1Val and self.input2Val

        super().Simulate()

class OrGate(Component):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, screen):
        # Scale the sprite to the width and height of the component, then draw
        scaled_sprite = pygame.transform.scale(images[1], (self.width, self.height))
        rect = scaled_sprite.get_rect(center=(self.x, self.y))
        screen.blit(scaled_sprite, rect)
    
    def Simulate(self):
        self.outputVal = self.input1Val or self.input2Val

        super().Simulate()

class NotGate(Component):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, True)

    def draw(self, screen):
        # Scale the sprite to the width and height of the component, then draw
        scaled_sprite = pygame.transform.scale(images[2], (self.width, self.height))
        rect = scaled_sprite.get_rect(center=(self.x, self.y))
        screen.blit(scaled_sprite, rect)
    
    def Simulate(self):
        self.outputVal = not self.input1Val

        super().Simulate()

class NorGate(Component):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, screen):
        # Scale the sprite to the width and height of the component, then draw
        scaled_sprite = pygame.transform.scale(images[3], (self.width, self.height))
        rect = scaled_sprite.get_rect(center=(self.x, self.y))
        screen.blit(scaled_sprite, rect)

    def Simulate(self):
        self.outputVal = not (self.input1Val or self.input2Val)

        super().Simulate()

class XorGate(Component):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, screen):
        # Scale the sprite to the width and height of the component, then draw
        scaled_sprite = pygame.transform.scale(images[4], (self.width, self.height))
        rect = scaled_sprite.get_rect(center=(self.x, self.y))
        screen.blit(scaled_sprite, rect)
    
    def Simulate(self):
        self.outputVal = self.input1Val != self.input2Val

        super().Simulate()

class NandGate(Component):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, screen):
        # Scale the sprite to the width and height of the component, then draw
        scaled_sprite = pygame.transform.scale(images[5], (self.width, self.height))
        rect = scaled_sprite.get_rect(center=(self.x, self.y))
        screen.blit(scaled_sprite, rect)

    def Simulate(self):
        self.outputVal = not (self.input1Val and self.input2Val)

        super().Simulate()

class CircuitInput(Component):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, screen):
        if not self.outputVal:
            self.colour = (105, 105, 100)
        else:
            self.colour = (26, 240, 37)
        super().draw(screen)
    
    def drawInputs(self, screen):
        pass
    #FINALLY FOUND A USE FOR PASS STATEMENT

    def is_input1_hovered(self, mouse_pos):
        return False
    
    def is_input2_hovered(self, mouse_pos):
        return False
    
    def Simulate(self):
        super().Simulate()
    
class CircuitOutput(Component):

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, True)

    def draw(self, screen):
        if not self.input1Val:
            self.colour = (105, 105, 100)
        else:
            self.colour = (26, 240, 37)
        super().draw(screen)
    
    def drawOutputs(self, screen):
        pass

    def is_output_hovered(self, mouse_pos):
        return False

    def Simulate(self):
        pass
    


# Create a list to store multiple components
components = []



# Variable to store the currently dragged component
cur_comp = None

SimulationMode = False
enterKeyPress = False
componentSelected = False
OutputSelected = False

currentComponentToBeCreated = 0

# Game loop
while True:

    # Get the current mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Check if RMB is held down
    mouse_buttons = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not SimulationMode and event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                currentComponentToBeCreated = min(currentComponentToBeCreated+1, 5)
            elif event.y == -1:
                currentComponentToBeCreated = max(currentComponentToBeCreated-1, 0)

        elif event.type == pygame.KEYDOWN:
            cur_comp = None
            if event.key == pygame.K_s and not SimulationMode:
                SimulationMode = True
                componentSelected = False
                OutputSelected = False
            elif event.key == pygame.K_c and SimulationMode:
                SimulationMode = False
                componentSelected = False
                OutputSelected = False
                for component in components:
                    component.reset()
            elif event.key == pygame.K_m:   #code for making the components
                if currentComponentToBeCreated == 0:
                    components.append(AndGate(mouse_pos[0], mouse_pos[1], 85, 55))
                elif currentComponentToBeCreated == 1:
                    components.append(OrGate(mouse_pos[0], mouse_pos[1], 85, 55))
                elif currentComponentToBeCreated == 2:
                    components.append(NotGate(mouse_pos[0], mouse_pos[1], 85, 55))
                elif currentComponentToBeCreated == 3:
                    components.append(NorGate(mouse_pos[0], mouse_pos[1], 85, 55))
                elif currentComponentToBeCreated == 4:
                    components.append(XorGate(mouse_pos[0], mouse_pos[1], 85, 55))
                elif currentComponentToBeCreated == 5:
                    components.append(NandGate(mouse_pos[0], mouse_pos[1], 85, 55))
            elif event.key == pygame.K_i:
                components.append(CircuitInput(mouse_pos[0], mouse_pos[1], 82, 55))
            elif event.key == pygame.K_o:
                components.append(CircuitOutput(mouse_pos[0], mouse_pos[1], 82, 55))
            elif event.key == pygame.K_RETURN:  #for advancing the simulation
                enterKeyPress = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                enterKeyPress = False
            



    

    #CODE FOR COMPONENT EDITOR MODE
    if not SimulationMode:
        if mouse_buttons[0]:  # LMB is pressed
            if cur_comp is None:
                # Find the first component under the mouse
                for component in components:
                    if component.is_hovered(mouse_pos) and not OutputSelected:
                        cur_comp = component
                        componentSelected = True
                        OutputSelected = False
                        break
                    elif component.is_output_hovered(mouse_pos) and not componentSelected:
                        cur_comp = component
                        OutputSelected = True
                        componentSelected = False
                        break
            if cur_comp is not None:
                # Move the current component with the mouse
                if componentSelected:
                    cur_comp.UpdatePos(mouse_pos)
                elif OutputSelected:
                    for component in components:
                        if component.is_input1_hovered(mouse_pos) and (cur_comp is not component):
                            if [component, 1] not in cur_comp.outputs:
                                #above condition is to prevent making multiple wires to same input
                                cur_comp.outputs.append([component, 1])
                                cur_comp = None
                                OutputSelected = False
                                break
                        elif component.is_input2_hovered(mouse_pos) and (cur_comp is not component):
                            if [component, 2] not in cur_comp.outputs and (not component.singleInput):
                                cur_comp.outputs.append([component, 2])
                                cur_comp = None
                                OutputSelected = False
                                break

        elif mouse_buttons[2]:  # RMB is pressed
            for component in components:
                if component.is_output_hovered(mouse_pos):
                    component.outputs.clear()
                    break
                elif component.is_hovered(mouse_pos):
                    for comp in components:
                        for componentLink in comp.outputs:
                            if componentLink[0] is component:
                                comp.outputs.remove(componentLink)
                    components.remove(component)    #delete the component
                    break
        else:
            cur_comp = None # Release the component when RMB is released
            componentSelected = False
    
    
    else:   #CODE FOR SIMULATION MODE
        for component in components:
            if enterKeyPress:
                component.Simulate()
            if isinstance(component, CircuitInput) and component.is_hovered(mouse_pos):
                if mouse_buttons[0]:
                    component.outputVal = True
                elif mouse_buttons[2]:
                    component.outputVal = False




    # Clear screen
    screen.fill((255, 255, 255))
    
    # Draw all components
    for component in reversed(components):
        component.draw(screen)
        if not SimulationMode:
            component.input1colour = (105, 105, 100)
            component.input2colour = (105, 105, 100)

            component.outputcolour = (105, 105, 100)

            if (cur_comp is not None) and not SimulationMode:
                cur_comp.outputcolour = (228, 240, 58)
                pygame.draw.line(screen, (20, 20, 20), (int(cur_comp.outputxy[0]), int(cur_comp.outputxy[1])), (mouse_pos[0], mouse_pos[1]), 2)
            
        else:
            if component.input1Val:
                component.input1colour = (26, 240, 37)
            else:
                component.input1colour = (105, 105, 100)
            
            if component.input2Val:
                component.input2colour = (26, 240, 37)
            else:
                component.input2colour = (105, 105, 100)

            if component.outputVal:
                component.outputcolour = (26, 240, 37)
            else:
                component.outputcolour = (105, 105, 100)

        component.drawInputs(screen)
        component.drawOutputs(screen)

    screen.blit(pygame.transform.scale(images[currentComponentToBeCreated], (59, 37)), (0,0))

    pygame.draw.line(screen, (70, 185, 219), (0, 39), (61, 39), 2)
    pygame.draw.line(screen, (70, 185, 219), (61, 0), (61, 39), 2)

    # Update the display
    pygame.display.flip()

    # Frame rate control
    pygame.time.Clock().tick(60)
import pygame
import math
import random
import datetime
# you will need to install pygame widgets before using this
# type "pip install pygamewidgets" into the shell
#https://pygamewidgets.readthedocs.io/en/latest/widgets/button/
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
# Initialize Pygame
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Recursive Tree")
surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0, 5)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 150, 0)
BROWN = (150, 75, 0)

# Creates the button with optional parameters
def buttClick():
    global count
    savedfilename = "screenshot"+str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))+".jpeg"
    print("Screen shot saved as "+savedfilename)
    # pygame.image.save(screen, savedfilename)
    count = 0

button = Button(
    # Mandatory Parameters
    screen,  # Surface to place button on
    650,  # X-coordinate of top left corner
    5,  # Y-coordinate of top left corner
    150,  # Width
    50,  # Height

    # Optional Parameters
    text='Save Screenshot',  # Text to display
    fontSize=16,  # Size of font
    margin=2,  # Minimum distance between text/image and edge of button
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=10,  # Radius of border corners (leave empty for not curved)
    onClick=buttClick  # Function to call when clicked on
)

# puts two sliders on the bottom of the screen to control the number of levels and
# the length of the branches
# number of levels
levelslider = Slider(screen, 520, 720, 200, 20, min=0, max=199, step=1,   colour=RED, handleColour=BLUE)
leveloutput = TextBox(screen, 530, 750, 50, 50, fontSize=20)
leveloutput.disable()  # Act as label instead of textbox
# length of branches
branchlenslider = Slider(screen, 20, 720, 200, 20, min=0, max=15, step=1,   colour=RED, handleColour=BLUE)
branchlenoutput = TextBox(screen, 30, 750, 50, 50, fontSize=20)
branchlenoutput.disable()  # Act as label instead of textbox

class Branch:
    """each branch has a start point (x,y) an angle, a length and a thickness"""
    def __init__(self, x1, y1, angle, length, thickness):
        self.x1 = x1
        self.y1 = y1
        self.angle = angle
        self.length = length
        self.thickness = thickness

    def draw(self):
        """Draws the branch on the screen."""
        angle = math.radians(self.angle)
        # calculates the end point of the branch using trig
        x2 = self.x1 + self.length * math.cos(angle)
        y2 = self.y1 + self.length * math.sin(angle)
        # draws line between points
        pygame.draw.line(surface, cp.get_color(), (self.x1, self.y1), (x2, y2), self.thickness)

    def grow(self, levels):
        """Recursively grows branches."""
        if levels > 0: #base case
            # Grow left branch
            # you could tweak the numbers in brackets to control randomness
            # could add more sliders for this?
            left_angle = self.angle - random.randint(15, 30)
            left_length = self.length * random.uniform(0.6, 0.8)
            left_branch = Branch(self.x1 + self.length * math.cos(math.radians(self.angle)),
                                 self.y1 + self.length * math.sin(math.radians(self.angle)),
                                 left_angle, left_length, self.thickness-1)
            left_branch.draw()
            left_branch.grow(levels - 1)

            # Grow right branch
            right_angle = self.angle + random.randint(15, 30)
            right_length = self.length * random.uniform(0.6, 0.8)
            right_branch = Branch(self.x1 + self.length * math.cos(math.radians(self.angle)),
                                 self.y1 + self.length * math.sin(math.radians(self.angle)),
                                 right_angle, right_length, self.thickness-1)
            right_branch.draw()
            right_branch.grow(levels - 1)

# Color Picker From stack overflow
# https://stackoverflow.com/questions/73517832/how-to-make-an-color-picker-in-pygame


class ColorPicker:
    def __init__(self, x, y, w, h):
        # this draws the slider
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h))
        self.image.fill((255, 255, 255))
        self.rad = h//2
        self.pwidth = w-self.rad*2
        for i in range(self.pwidth):
            color = pygame.Color(0)
            color.hsla = (int(360*i/self.pwidth), 100, 60, 100)
            pygame.draw.rect(self.image, color, (i+self.rad, h//3, 1, h-2*h//3))
        self.p = 0

    def get_color(self):
        """this gets the color based on where the slider is on the ruler"""
        color = pygame.Color(0)
        color.hsla = (int(self.p * self.pwidth), 100, 60, 100)
        return color

    def update(self):
        """sets the attribute p to where the mouse is clicked on slider"""
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))

    def draw(self, surf):
        """draws the slider circle on the rectangle in the chosen color"""
        surf.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(surf, self.get_color(), center, self.rect.height // 2)


cp = ColorPicker(50, 50, 360, 30) # Draw Color Picker to screen
cpText = TextBox(screen, 30, 20, 200, 25, fontSize=15)
cpText.setText("Drag to choose colour")


def draw_the_tree():
    """function to actually draw the tree and start the recursion"""
    global count # this variable name could be better!
    if count == 0:
        # Draw the tree
        trunk = Branch(SCREEN_WIDTH // 2, SCREEN_HEIGHT, -85, levelslider.getValue(), branchlenslider.getValue())  # Initial trunk
        trunk.draw()
        trunk.grow(branchlenslider.getValue())
        count = 1 # sets count to 1 so it wont draw again until the button is clicked


count = 0
# ---------------------Main Game Loop-----------------------
running = True
while running:
    events = pygame.event.get()
    # ------------------- listen out for events ---------------------------
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    # ------------------ end checking for events --------------------------
    screen.fill(WHITE)  # Clear the screen

    draw_the_tree()  # only draws the tree if count = 0 which is set by the button

    cp.draw(screen)  # draw color picker

    leveloutput.setText(levelslider.getValue())  # print out number of levels selected
    branchlenoutput.setText(branchlenslider.getValue())  # print out branch length selected
    
    pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
    cp.update()  # render color picker and listens for a drag

    screen.blit(surface, (0, 0))
    pygame.display.flip()  # Update the display
    clock.tick(30)

pygame.quit()

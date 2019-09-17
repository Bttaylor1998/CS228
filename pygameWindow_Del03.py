import pygame
from constants import *
class PYGAME_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((pygameWindowWidth,pygameWindowHeight))

    def Prepare(self):
        self.screen.fill((255, 255, 255))

    def Reveal(self):
        pygame.display.update()

    def Draw_Black_Circle(self, x, y):
        pygame.draw.circle(self.screen, (0,0,0), (x,y), 10, 0)

    def Draw_Line(self, color, xBase, yBase, xTip, yTip, width):
        pygame.draw.line(self.screen, color, (xBase,yBase), (xTip,yTip), 1)

from pygameWindow import PYGAME_WINDOW
import random as r
pygameWindow = PYGAME_WINDOW()
x = 500
y = 250

def Perturb_Circle_Position():
    global x, y
    fourSidedDieRoll = r.randint(1,4)
    if (fourSidedDieRoll == 1):
        x = x - 1
    elif (fourSidedDieRoll == 2):
        x = x + 1
    elif (fourSidedDieRoll == 3):
        y = y - 1
    elif (fourSidedDieRoll == 4):
        y = y + 1

while True:
    pygameWindow.Prepare()
    pygameWindow.Draw_Black_Circle(x,y)
    pygameWindow.Reveal()
    Perturb_Circle_Position()

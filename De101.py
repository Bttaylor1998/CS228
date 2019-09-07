import sys
sys.path.insert(0, '..')
import Leap
from constants import *
from pygameWindow import PYGAME_WINDOW
##import random as r
pygameWindow = PYGAME_WINDOW()
x = 300
y = 100

xMin = 1000.0
xMax = -1000.0
yMin = 1000.0
yMax = -1000.0

controller = Leap.Controller()

def Scale_Val(val, leapMin, leapMax, pygameMin, pygameMax):
    leapRange = leapMax - leapMin
    pygameRange = pygameMax - pygameMin
    if (leapRange == 0):
        scaledVal = pygameMin
    else:
        scaledVal = (((val - leapMin) * pygameRange) / leapRange) + pygameMin
    return scaledVal
                 
    
def Handle_Frame(frame):
    global x, y, xMin, xMax, yMin, yMax
    hand = frame.hands[0]
    fingers = hand.fingers
    indexFingerList = fingers.finger_type(Leap.Finger.TYPE_INDEX)
    indexFinger = indexFingerList[0]
    distalPhalanx = indexFinger.bone(Leap.Bone.TYPE_DISTAL)
    tip = distalPhalanx.next_joint
    print(tip)
    x = int(tip[0])
    y = int(tip[1])
    if (x < xMin):
        xMin = x
    if (x > xMax):
        xMax = x
    if (y < yMin):
        yMin = y
    if (y > yMax):
        yMax = y

    print(xMin)
    print(xMax)
    print(yMin)
    print(yMax)

while True:
    pygameWindow.Prepare()
    frame = controller.frame()
    if (len(frame.hands) > 0):
        Handle_Frame(frame)
        pygameX = Scale_Val(x, xMin, xMax, 0, pygameWindowWidth)
        pygameY = Scale_Val(y, yMax, yMin, 0, pygameWindowHeight)
        pygameWindow.Draw_Black_Circle(pygameX,pygameY)
        print(pygameX)
        print(pygameY)
    pygameWindow.Reveal()
##    Perturb_Circle_Position()

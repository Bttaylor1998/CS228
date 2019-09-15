import sys
sys.path.insert(0, '..')
import Leap
from pygameWindow_Del03 import PYGAME_WINDOW
from constants import *

class Deliverable:
    def __init__(self):
        self.pygameWindow = PYGAME_WINDOW()
        self.xMin = 100.0
        self.xMax = -100.0
        self.yMin = 100.0
        self.yMax = -100.0
        self.controller = Leap.Controller()

    def Scale_Val(self, val, leapMin, leapMax, pygameMin, pygameMax):
        leapRange = leapMax - leapMin
        pygameRange = pygameMax - pygameMin
        if (leapRange == 0):
            scaledVal = pygameMin
        else:
            scaledVal = (((val - leapMin) * pygameRange) / leapRange) + pygameMin
        return scaledVal
    
    def Handle_Frame(self, frame):
        global x, y, xMin, xMax, yMin, yMax
        hand = frame.hands[0]
        fingers = hand.fingers
        for fing in fingers:
            self.Handle_Finger(fing)

    def Handle_Finger(self, finger):
        for b in range(4):
            self.Handle_Bone(finger.bone(b), b)

    def Handle_Bone(self, bone, b):
        base = bone.prev_joint
        tip = bone.next_joint

        xBase, yBase = self.Handle_Vector_From_Leap(base)
        xTip, yTip = self.Handle_Vector_From_Leap(tip)

        xBase = self.Scale_Val(xBase, self.xMin, self.xMax, 0, pygameWindowWidth)
        yBase = self.Scale_Val(yBase, self.yMin, self.yMax, 0, pygameWindowHeight)
        xTip = self.Scale_Val(xTip, self.xMin, self.xMax, 0, pygameWindowWidth)
        yTip = self.Scale_Val(yTip, self.yMin, self.yMax, 0, pygameWindowHeight)

        if(self.numberOfHands == 1):
            self.pygameWindow.Draw_Line((124,252,0), xBase, yBase, xTip, yTip, b)
        elif(self.numberOfHands == 2):
            self.pygameWindow.Draw_Line((255,0,0), xBase, yBase, xTip, yTip, b)

    def Handle_Vector_From_Leap(self, v):
        x = v[0]
        y = v[2]
        if (x < self.xMin):
            self.xMin = x
        if (x > self.xMax):
            self.xMax = x
        if (y < self.yMin):
            self.yMin = y
        if (y > self.yMax):
            self.yMax = y
        return x,y

    def Run_Forever(self):
        while True:
            self.Run_Once()

    def Run_Once(self):
        self.pygameWindow.Prepare()
        frame = self.controller.frame()
        self.numberOfHands  = len(frame.hands)
        if (self.numberOfHands > 0):
            self.Handle_Frame(frame)
        self.pygameWindow.Reveal()

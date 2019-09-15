import sys
sys.path.insert(0, '..')
import Leap
from pygameWindow_Del03 import PYGAME_WINDOW
from constants import *
import numpy as np
import pickle
import os
import shutil

class Deliverable:
    def __init__(self):
        self.pygameWindow = PYGAME_WINDOW()
        self.xMin = 100.0
        self.xMax = -100.0
        self.yMin = 100.0
        self.yMax = -100.0
        self.controller = Leap.Controller()
        self.previousNumberOfHands = 0
        self.currentNumberOfHands = 0
        self.gestureData = np.zeros((5,4,6),dtype='f')
        self.gestureNum = 0
        self.Clear_User_Data()

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
        if self.Recording_Is_Ending():
            print(self.gestureData)
            self.Save_Gesture()

    def Handle_Finger(self, finger):
        for b in range(5):
            for bone in range(4):
                self.Handle_Bone(finger.bone(bone), bone, b)

    def Handle_Bone(self, bone, boneNum, b):
        base = bone.prev_joint
        tip = bone.next_joint

        xBase, yBase = self.Handle_Vector_From_Leap(base)
        xTip, yTip = self.Handle_Vector_From_Leap(tip)

        xBase = self.Scale_Val(xBase, self.xMin, self.xMax, 0, pygameWindowWidth)
        yBase = self.Scale_Val(yBase, self.yMin, self.yMax, 0, pygameWindowHeight)
        xTip = self.Scale_Val(xTip, self.xMin, self.xMax, 0, pygameWindowWidth)
        yTip = self.Scale_Val(yTip, self.yMin, self.yMax, 0, pygameWindowHeight)

        if(self.currentNumberOfHands == 1):
            self.pygameWindow.Draw_Line((124,252,0), xBase, yBase, xTip, yTip, b)
            if self.Recording_Is_Ending():
                self.gestureData[b, boneNum, 0] = base[0]
                self.gestureData[b, boneNum, 1] = base[1]
                self.gestureData[b, boneNum, 2] = base[2]
                self.gestureData[b, boneNum, 3] = tip[0]
                self.gestureData[b, boneNum, 4] = tip[1]
                self.gestureData[b, boneNum, 5] = tip[2]
            
        elif(self.currentNumberOfHands == 2):
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
        self.currentNumberOfHands = len(frame.hands)
        if (self.currentNumberOfHands > 0):
            self.Handle_Frame(frame)
        self.pygameWindow.Reveal()
        self.previousNumberOfHands = self.currentNumberOfHands

    def Recording_Is_Ending(self):
        if(self.currentNumberOfHands == 1 and self.previousNumberOfHands == 2):
            return True

    def Save_Gesture(self):
        pickle_out = open("userData/gesture" + str(self.gestureNum) + ".p", "wb")
        pickle.dump(self.gestureData, pickle_out)
        pickle_out.close()
        self.gestureNum += 1

    def Clear_User_Data(self):
        shutil.rmtree('userData')
        os.mkdir('userData')

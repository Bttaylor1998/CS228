import sys
sys.path.insert(0, '..')
import Leap
from pygameWindow_Del03 import PYGAME_WINDOW
from constants import *
import numpy as np
import pickle
import os
import shutil

class Recorder:
    def __init__(self):
        self.pygameWindow = PYGAME_WINDOW()
        self.numberOfGestures = 1000;
        self.gestureIndex = 0;
        self.xMin = 1000.0
        self.xMax = -1000.0
        self.yMin = 1000.0
        self.yMax = -1000.0
        self.controller = Leap.Controller()
        self.previousNumberOfHands = 0
        self.currentNumberOfHands = 0
        self.gestureData = np.zeros((5,4,6,self.numberOfGestures),dtype='f')
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
            idNum = fing.type
            self.Handle_Finger(fing, idNum)
        if self.currentNumberOfHands == 2:
            print('gesture' + str(self.gestureIndex) + ' stored.')
            self.gestureIndex = self.gestureIndex + 1
            if self.gestureIndex == self.numberOfGestures:
                self.Save_Gesture()
                exit(0)

    def Handle_Finger(self, finger, i):
        for j in range(4):
            self.Handle_Bone(finger.bone(j), i, j)

    def Handle_Bone(self, bone, i, j):
        base = bone.prev_joint
        tip = bone.next_joint

        xBase, yBase = self.Handle_Vector_From_Leap(base)
        xTip, yTip = self.Handle_Vector_From_Leap(tip)

        xBase = self.Scale_Val(xBase, self.xMin, self.xMax, 0, pygameWindowWidth)
        yBase = self.Scale_Val(yBase, self.yMin, self.yMax, 0, pygameWindowHeight)
        xTip = self.Scale_Val(xTip, self.xMin, self.xMax, 0, pygameWindowWidth)
        yTip = self.Scale_Val(yTip, self.yMin, self.yMax, 0, pygameWindowHeight)

        if(self.currentNumberOfHands == 1):
            self.pygameWindow.Draw_Line((124,252,0), xBase, yBase, xTip, yTip, i)
##            if self.Recording_Is_Ending():
##                print(base.x, base.y, base.z, tip.x, tip.y, tip.z)
##                self.gestureData[i,j,0] = base.x
##                self.gestureData[i,j,1] = base.y
##                self.gestureData[i,j,2] = base.z
##                self.gestureData[i,j,3] = tip.x
##                self.gestureData[i,j,4] = tip.y
##                self.gestureData[i,j,5] = tip.z
##            
        if(self.currentNumberOfHands == 2):
            self.pygameWindow.Draw_Line((255,0,0), xBase, yBase, xTip, yTip, i)
            self.gestureData[i,j,0,self.gestureIndex] = base.x
            self.gestureData[i,j,1,self.gestureIndex] = base.y
            self.gestureData[i,j,2,self.gestureIndex] = base.z
            self.gestureData[i,j,3,self.gestureIndex] = tip.x
            self.gestureData[i,j,4,self.gestureIndex] = tip.y
            self.gestureData[i,j,5,self.gestureIndex] = tip.z

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
        pickle_out = open("userData/gesture.p", "wb")
        pickle.dump(self.gestureData, pickle_out)
        pickle_out.close()

    def Clear_User_Data(self):
        shutil.rmtree('userData')
        os.mkdir('userData')

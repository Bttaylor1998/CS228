import numpy as np
import pickle
import os
from pygameWindow_Del03 import PYGAME_WINDOW
from constants import *
import time

class READER:
    def __init__(self):
        self.Get_Num_Gestures()
        self.pygameWindow = PYGAME_WINDOW()

    def Get_Num_Gestures(self):
        path, dirs, files = next(os.walk('userData'))
        self.numGestures = len(files)

    def Print_Gestures(self):
        for i in range (0, self.numGestures-1):
            pickle_in  = open("userData/gesture" + str(i) + ".p", "rb")
            gestureData = pickle.load(pickle_in)
            print (gestureData)

    def Draw_Gestures(self):
        while True:
            self.Draw_Each_Gesture_Once()

    def Draw_Each_Gesture_Once(self):
        for i in range (0, self.numGestures-1):
            self.pygameWindow.Prepare()
            pickle_in  = open("userData/gesture" + str(i) + ".p", "rb")
            gestureData = pickle.load(pickle_in)
            for i in range(5):
                for j in range(4):
                    currentBone = gestureData[i, j,:]
                    xBaseNotYetScaled = gestureData[i,j,0]
                    yBaseNotYetScaled = gestureData[i,j,2]
                    xTipNotYetScaled = gestureData[i,j,3]
                    yTipNotYetScaled = gestureData[i,j,5]

##                    self.pygameWindow.Draw_Line((51,51,255),xBaseNotYetScaled, yBaseNotYetScaled, xTipNotYetScaled, yTipNotYetScaled, 1)

                    xBase = self.Scale_Val(xBaseNotYetScaled, -100, 100, 0, pygameWindowWidth)
                    yBase = self.Scale_Val(yBaseNotYetScaled, -100, 100, 0, pygameWindowHeight)
                    xTip = self.Scale_Val(xTipNotYetScaled, -100, 100, 0, pygameWindowWidth)
                    yTip = self.Scale_Val(yTipNotYetScaled, -100, 100, 0, pygameWindowHeight)
                    self.pygameWindow.Draw_Line((51,51,255),xBase, yBase, xTip, yTip, 1)
                    self.Draw_Gesture(i)
                    self.pygameWindow.Reveal()
                    time.sleep(0.1)
            
    def Draw_Gesture(self, gesture):
        pass

    def Scale_Val(self, val, leapMin, leapMax, pygameMin, pygameMax):
        leapRange = leapMax - leapMin
        pygameRange = pygameMax - pygameMin
        if (leapRange == 0):
            scaledVal = pygameMin
        else:
            scaledVal = (((val - leapMin) * pygameRange) / leapRange) + pygameMin
        return scaledVal

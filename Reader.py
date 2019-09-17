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
        self.xMin = 1000.0
        self.xMax = -1000.0
        self.yMin = 1000.0
        self.yMax = -1000.0

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
        for i in range (0, self.numGestures):
            self.Draw_Gesture(i)

    def Draw_Gesture(self, g):
        self.pygameWindow.Prepare()
        pickle_in  = open("userData/gesture" + str(g) + ".p", "rb")
        gestureData = pickle.load(pickle_in)
        for i in range(5):
            for j in range(4):
                currentBone = gestureData[i, j,:]
                xBaseNotYetScaled = gestureData[i,j,0]
                yBaseNotYetScaled = gestureData[i,j,2]
                xTipNotYetScaled = gestureData[i,j,3]
                yTipNotYetScaled = gestureData[i,j,5]
                xBase = self.Scale_Val(xBaseNotYetScaled, self.xMax, self.xMin, 0, pygameWindowWidth)
                yBase = self.Scale_Val(yBaseNotYetScaled, self.yMax, self.yMin, 0, pygameWindowHeight)
                xTip = self.Scale_Val(xTipNotYetScaled, self.xMax, self.xMin, 0, pygameWindowWidth)
                yTip = self.Scale_Val(yTipNotYetScaled, self.yMax, self.yMin, 0, pygameWindowHeight)
                self.pygameWindow.Draw_Line((0,0,255), xBase, yBase, xTip, yTip, 1)
        self.pygameWindow.Reveal()
        time.sleep(1.0)

    def Scale_Val(self, val, leapMin, leapMax, pygameMin, pygameMax):
        leapRange = leapMax - leapMin
        pygameRange = pygameMax - pygameMin
        if (leapRange == 0):
            scaledVal = pygameMin
        else:
            scaledVal = (((val - leapMin) * pygameRange) / leapRange) + pygameMin
        return scaledVal

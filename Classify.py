from knn import KNN
import numpy as np
import pickle

knn = KNN()

pickle_in  = open("userData/trainM.p", "rb")
trainM = pickle.load(pickle_in)

pickle_in  = open("userData/trainN.p", "rb")
trainN = pickle.load(pickle_in)

pickle_in  = open("userData/testM.p", "rb")
testM = pickle.load(pickle_in)

pickle_in  = open("userData/testN.p", "rb")
testN = pickle.load(pickle_in)

def CenterData(X):
    allXCoordinates = X[:,:,0,:]
    meanValue = allXCoordinates.mean()
    X[:,:,0,:] = allXCoordinates - meanValue
    allYCoordinates = X[:,:,1,:]
    meanValueY = allYCoordinates.mean()
    X[:,:,1,:] =  allYCoordinates - meanValueY
##    allZCoordinates = X[:,:,2,:]
##    meanValueZ = allZCoordinates.mean()
##    X[:,:,2,:] = allZCoordinates - meanValueZ
    return X

def ReduceData(X):
    X = np.delete(X,1,1)
    X = np.delete(X,1,1)
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    return X

def ReshapeData(set1, set2):
    X = np.zeros((2000,5*2*3),dtype='f')
    y = np.zeros(2000,dtype='f')
    for row in range(0,1000):
        y[row] = 0
        y[row+1000] = 1
        col = 0
        for finger in range(0,5):
            for bone in range(0,2):
                for joint in range(0,3):
                    X[row,col] = set1[finger,bone,joint,row]
                    X[row+1000,col] = set2[finger,bone,joint,row]
                    col = col + 1
    return X, y

trainM = ReduceData(trainM)
trainN = ReduceData(trainN)
testM = ReduceData(testM)
testN = ReduceData(testN)

trainM = CenterData(trainM)
trainN = CenterData(trainN)
testM = CenterData(testM)
testN = CenterData(testN)

trainX, trainy = ReshapeData(trainM, trainN)
testX, testy = ReshapeData(testM, testN)

knn.Use_K_Of(15)
knn.Fit(trainX, trainy)

counter = 0
for row in range(2000):
    prediction = knn.Predict(testX[row,:])
    if prediction == testy[row]:
        counter = counter + 1
print((counter/2000)*100)

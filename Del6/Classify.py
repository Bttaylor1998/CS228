from knn import KNN
import numpy as np
import pickle

knn = KNN()

pickle_in  = open("userData/trainM.p", "rb")
train0 = pickle.load(pickle_in)

pickle_in  = open("userData/trainN.p", "rb")
train1 = pickle.load(pickle_in)

pickle_in  = open("userData/testM.p", "rb")
test0 = pickle.load(pickle_in)

pickle_in  = open("userData/testN.p", "rb")
test1 = pickle.load(pickle_in)

train2 = pickle.load(open('userData/Liu_train2.p','rb'))
test2 = pickle.load(open('userData/Liu_test2.p','rb'))

train3 = pickle.load(open('userData/Liu_train3.p','rb'))
test3 = pickle.load(open('userData/Liu_test3.p','rb'))

train4 = pickle.load(open('userData/Ward_train4.p','rb'))
test4 = pickle.load(open('userData/Ward_test4.p','rb'))

train5 = pickle.load(open('userData/Boland_train5.p','rb'))
test5 = pickle.load(open('userData/Boland_test5.p','rb'))

train6 = pickle.load(open('userData/Boland_train6.p','rb'))
test6 = pickle.load(open('userData/Boland_test6.p','rb'))

train7 = pickle.load(open('userData/MacMaster_train7.p','rb'))
test7 = pickle.load(open('userData/MacMaster_test7.p','rb'))

train8 = pickle.load(open('userData/Zhang_train8.p','rb'))
test8 = pickle.load(open('userData/Zhang_test8.p','rb'))

train9 = pickle.load(open('userData/Saulean_train9.p','rb'))
test9 = pickle.load(open('userData/Saulean_test9.p','rb'))

def CenterData(X):
    allXCoordinates = X[:,:,0,:]
    meanValue = allXCoordinates.mean()
    X[:,:,0,:] = allXCoordinates - meanValue
    allYCoordinates = X[:,:,1,:]
    meanValueY = allYCoordinates.mean()
    X[:,:,1,:] =  allYCoordinates - meanValueY
    allZCoordinates = X[:,:,2,:]
    meanValueZ = allZCoordinates.mean()
    X[:,:,2,:] = allZCoordinates - meanValueZ
    return X

def ReduceData(X):
    X = np.delete(X,1,1)
    X = np.delete(X,1,1)
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    return X

def ReshapeData(set1,set2,set3,set4,set5,set6,set7,set8,set9,set10):
    X = np.zeros((10000,5*2*3),dtype='f')
    y = np.zeros(10000,dtype='f')
    for row in range(0,1000):
        y[row] = 0
        y[row+1000] = 1
        y[row+2000] = 2
        y[row+3000] = 3
        y[row+4000] = 4
        y[row+5000] = 5
        y[row+6000] = 6
        y[row+7000] = 7
        y[row+8000] = 8
        y[row+9000] = 9
        col = 0
        for finger in range(0,5):
            for bone in range(0,2):
                for joint in range(0,3):
                    X[row,col] = set1[finger,bone,joint,row]
                    X[row+1000,col] = set2[finger,bone,joint,row]
                    X[row+2000,col] = set3[finger,bone,joint,row]
                    X[row+3000,col] = set4[finger,bone,joint,row]
                    X[row+4000,col] = set5[finger,bone,joint,row]
                    X[row+5000,col] = set6[finger,bone,joint,row]
                    X[row+6000,col] = set7[finger,bone,joint,row]
                    X[row+7000,col] = set8[finger,bone,joint,row]
                    X[row+8000,col] = set9[finger,bone,joint,row]
                    X[row+9000,col] = set10[finger,bone,joint,row]
                    col = col + 1
    return X, y

train0 = ReduceData(train0)
train1 = ReduceData(train1)
train2 = ReduceData(train2)
train3 = ReduceData(train3)
train4 = ReduceData(train4)
train5 = ReduceData(train5)
train6 = ReduceData(train6)
train7 = ReduceData(train7)
train8 = ReduceData(train8)
train9 = ReduceData(train9)

test0 = ReduceData(test0)
test1 = ReduceData(test1)
test2 = ReduceData(test2)
test3 = ReduceData(test3)
test4 = ReduceData(test4)
test5 = ReduceData(test5)
test6 = ReduceData(test6)
test7 = ReduceData(test7)
test8 = ReduceData(test8)
test9 = ReduceData(test9)

train0 = CenterData(train0)
train1 = CenterData(train1)
train2 = CenterData(train2)
train3 = CenterData(train3)
train4 = CenterData(train4)
train5 = CenterData(train5)
train6 = CenterData(train6)
train7 = CenterData(train7)
train8 = CenterData(train8)
train9 = CenterData(train9)

test0 = CenterData(test0)
test1 = CenterData(test1)
test2 = CenterData(test2)
test3 = CenterData(test3)
test4 = CenterData(test4)
test5 = CenterData(test5)
test6 = CenterData(test6)
test7 = CenterData(test7)
test8 = CenterData(test8)
test9 = CenterData(test9)

trainX, trainy = ReshapeData(train0,train1,train2,train3,train4,train5,train6,train7,train8,train9)
testX, testy = ReshapeData(test0,test1,test2,test3,test4,test5,test6,test7,test8,test9)

knn.Use_K_Of(15)
knn.Fit(trainX, trainy)

counter = 0
for row in range(10000):
    prediction = knn.Predict(testX[row,:])
    if prediction == int(testy[row]):
        counter = counter + 1
        print(prediction, int(testy[row]), counter)
print((counter / 10000) * 100)

pickle.dump(knn, open('userData/classifier.p','wb'))
